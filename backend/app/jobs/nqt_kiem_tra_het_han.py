from backend.app import db
from backend.app.models.g6_hoi_vien import G6DangKyGoiTap
from backend.app.models.g6_nguoi_dung import G6NguoiDung
from backend.app.models.g6_thong_bao import G6ThongBao
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh
from backend.app.services.nqt_dich_vu_email import NqtDichVuEmail
from datetime import datetime, date, timedelta
import logging

nqt_logger = logging.getLogger(__name__)


def nqt_kiem_tra_goi_tap_het_han(nqt_app):
    """
    Background job: Kiểm tra các gói tập sắp hết hạn và gửi thông báo + email.
    Chạy mỗi ngày lúc 8:00 sáng.

    Đọc cấu hình số ngày nhắc trước từ DB (key: nqt_so_ngay_nhac_truoc, mặc định 3).
    """
    with nqt_app.app_context():
        try:
            # Lấy cấu hình số ngày nhắc trước từ DB
            nqt_so_ngay = NqtDichVuCauHinh.g6_lay('nqt_so_ngay_nhac_truoc', nqt_mac_dinh=3)
            nqt_so_ngay = int(nqt_so_ngay)

            nqt_ngay_moc = date.today() + timedelta(days=nqt_so_ngay)

            # Tìm các đăng ký đang hoạt động sắp hết hạn đúng N ngày nữa
            nqt_danh_sach = (
                db.session.query(G6DangKyGoiTap)
                .filter(
                    G6DangKyGoiTap.g6_ngay_het_han == nqt_ngay_moc,
                    G6DangKyGoiTap.g6_trang_thai == 'dang_hoat_dong',
                )
                .all()
            )

            nqt_da_gui = 0
            nqt_loi = 0

            for nqt_dang_ky in nqt_danh_sach:
                try:
                    nqt_hoi_vien = G6NguoiDung.query.get(nqt_dang_ky.g6_ma_nguoi_dung)
                    if not nqt_hoi_vien:
                        continue

                    nqt_ten_goi = (
                        nqt_dang_ky.g6_goi_tap.g6_ten_goi
                        if nqt_dang_ky.g6_goi_tap else f'Gói #{nqt_dang_ky.g6_ma_goi_tap}'
                    )

                    # Tạo thông báo trong hệ thống
                    nqt_thong_bao = G6ThongBao(
                        g6_loai='het_han_goi_tap',
                        g6_tieu_de='Gói tập sắp hết hạn',
                        g6_noi_dung=(
                            f'Hội viên {nqt_hoi_vien.g6_ho_ten} — gói "{nqt_ten_goi}" '
                            f'sẽ hết hạn vào ngày {nqt_dang_ky.g6_ngay_het_han}.'
                        ),
                        g6_ma_doi_tuong=nqt_hoi_vien.g6_ma_nguoi_dung,
                        g6_loai_doi_tuong='hoi_vien',
                        g6_ngay_tao=datetime.utcnow(),
                    )
                    db.session.add(nqt_thong_bao)

                    # Gửi email nếu hội viên có email
                    if nqt_hoi_vien.g6_email:
                        NqtDichVuEmail.nqt_gui_nhac_het_han(
                            nqt_email=nqt_hoi_vien.g6_email,
                            nqt_ho_ten=nqt_hoi_vien.g6_ho_ten,
                            nqt_ten_goi=nqt_ten_goi,
                            nqt_ngay_het_han=str(nqt_dang_ky.g6_ngay_het_han),
                            nqt_so_ngay=nqt_so_ngay,
                        )

                    nqt_da_gui += 1

                except Exception as nqt_e:
                    nqt_loi += 1
                    nqt_logger.error(
                        f'[Job] Lỗi xử lý đăng ký #{nqt_dang_ky.g6_ma_dang_ky}: {nqt_e}'
                    )

            db.session.commit()
            nqt_logger.info(
                f'[Job] Kiểm tra hết hạn hoàn tất: {nqt_da_gui} thông báo, {nqt_loi} lỗi.'
            )

        except Exception as nqt_e:
            nqt_logger.error(f'[Job] Lỗi nghiêm trọng trong job kiểm tra hết hạn: {nqt_e}')


def nqt_dong_bo_chuyen_khoan_job(nqt_app):
    """
    Background job: Quét các giao dịch MBBank từ checkgd.vn mỗi 15 giây
    để tự động xác nhận thanh toán các đơn hàng/thanh toán đang chờ xử lý.
    """
    import urllib.request
    import json
    with nqt_app.app_context():
        try:
            from backend.app.models.g6_don_hang import G6DonHang, G6LichSuDonHang
            from backend.app.models.g6_thanh_toan import G6ThanhToan
            
            pending_payments = G6ThanhToan.query.filter_by(g6_trang_thai='cho_xu_ly').all()
            pending_orders = G6DonHang.query.filter_by(g6_trang_thai='cho_xac_nhan').all()
            
            if not pending_payments and not pending_orders:
                return

            import os
            domain = os.environ.get('DOMAIN_CHECK', '')
            api_key = os.environ.get('API_KEY_CHECK', '')
            url = f"{domain}/api/v1/bank-transactions?api_key={api_key}&bank=MB&type=IN&page=1&limit=50"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode('utf-8'))

            if not res_data.get('status'):
                nqt_logger.error(f"[Job Chuyen Khoan] API checkgd.vn báo lỗi: {res_data.get('messages')}")
                return

            transactions = res_data.get('transactions', [])
            matched = False

            for trans in transactions:
                desc = trans.get('description', '')
                amount = float(trans.get('amount', 0))
                tx_id = trans.get('transaction_id')

                # 1. Match G6ThanhToan
                for tt in pending_payments:
                    if float(tt.g6_so_tien) == amount:
                        if str(tt.g6_ma_thanh_toan) in desc or f"HD{tt.g6_ma_thanh_toan}" in desc or f"GD{tt.g6_ma_thanh_toan}" in desc:
                            tt.g6_trang_thai = 'thanh_cong'
                            tt.g6_ngay_thanh_toan = datetime.utcnow()
                            tt.g6_ma_giao_dich_cong = tx_id
                            tt.g6_du_lieu_tra_ve = trans
                            
                            from backend.app.routes.nqt_thanh_toan import nqt_xuat_hoa_don
                            if not tt.g6_hoa_don:
                                nqt_xuat_hoa_don(tt)
                            matched = True

                # 2. Match G6DonHang
                for o in pending_orders:
                    if float(o.g6_tong_thanh_toan) == amount:
                        if str(o.g6_ma_don_hang) in desc or f"DH{o.g6_ma_don_hang}" in desc or f"DH-{o.g6_ma_don_hang}" in desc:
                            o.g6_trang_thai = 'dang_xu_ly'
                            
                            ls = G6LichSuDonHang(
                                g6_ma_don_hang=o.g6_ma_don_hang,
                                g6_trang_thai_moi='dang_xu_ly',
                                g6_ghi_chu=f"Xác nhận thanh toán tự động qua MBBank (Job ngầm), mã GD: {tx_id}",
                            )
                            db.session.add(ls)

                            new_tt = G6ThanhToan(
                                g6_ma_nguoi_dung=o.g6_ma_nguoi_dung,
                                g6_loai_giao_dich='don_hang',
                                g6_so_tien=amount,
                                g6_phuong_thuc='bank_transfer',
                                g6_trang_thai='thanh_cong',
                                g6_ma_giao_dich_cong=tx_id,
                                g6_du_lieu_tra_ve=trans,
                                g6_ngay_thanh_toan=datetime.utcnow(),
                                g6_ghi_chu=f"Tự động tạo từ đơn hàng #{o.g6_ma_don_hang}",
                            )
                            db.session.add(new_tt)
                            db.session.flush()
                            
                            from backend.app.routes.nqt_thanh_toan import nqt_xuat_hoa_don
                            nqt_xuat_hoa_don(new_tt)
                            matched = True

            if matched:
                db.session.commit()
                nqt_logger.info("[Job Chuyen Khoan] Đã tự động khớp và cập nhật thanh toán/đơn hàng thành công.")

        except Exception as e:
            nqt_logger.error(f"[Job Chuyen Khoan] Lỗi xử lý đồng bộ: {str(e)}")


def nqt_dang_ky_jobs(nqt_scheduler, nqt_app):
    """Đăng ký tất cả background jobs vào APScheduler."""

    # Job nhắc hết hạn gói tập — chạy mỗi ngày lúc 8:00 sáng
    nqt_scheduler.add_job(
        func=nqt_kiem_tra_goi_tap_het_han,
        args=[nqt_app],
        trigger='cron',
        hour=8,
        minute=0,
        id='nqt_job_kiem_tra_het_han',
        replace_existing=True,
        misfire_grace_time=3600,
    )
    nqt_logger.info('[Scheduler] Đã đăng ký job: nqt_job_kiem_tra_het_han (8:00 hàng ngày)')

    # Job đồng bộ chuyển khoản ngân hàng tự động — chạy mỗi 15 giây
    nqt_scheduler.add_job(
        func=nqt_dong_bo_chuyen_khoan_job,
        args=[nqt_app],
        trigger='interval',
        seconds=15,
        id='nqt_job_dong_bo_chuyen_khoan',
        replace_existing=True,
    )
    nqt_logger.info('[Scheduler] Đã đăng ký job: nqt_job_dong_bo_chuyen_khoan (mỗi 15 giây)')
