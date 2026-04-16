from backend.app import db
from backend.app.models.g6_hoi_vien import G6HoiVien, G6DangKyGoiTap
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
                    nqt_hoi_vien = G6HoiVien.query.get(nqt_dang_ky.g6_ma_hoi_vien)
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
                        g6_ma_doi_tuong=nqt_hoi_vien.g6_ma_hoi_vien,
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
        misfire_grace_time=3600,  # bỏ qua nếu trễ hơn 1 giờ
    )

    nqt_logger.info('[Scheduler] Đã đăng ký job: nqt_job_kiem_tra_het_han (8:00 hàng ngày)')
