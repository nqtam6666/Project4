from flask import Blueprint, request
from backend.app import db
from backend.app.models.nqt_thong_bao import NqtThongBao, NqtLichGuiThongBao
from backend.app.utils.nqt_phan_hoi import nqt_ok, nqt_loi
from backend.app.utils.nqt_xac_thuc import nqt_yeu_cau_dang_nhap
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

nqt_thong_bao_bp = Blueprint('nqt_thong_bao', __name__, url_prefix='/api')


@nqt_thong_bao_bp.route('/nqt-thong-bao', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_thong_bao():
    nqt_loai_nd = request.args.get('nqt_loai_nguoi_nhan')
    nqt_nd_id = request.args.get('nqt_ma_nguoi_nhan', type=int)
    nqt_q = NqtThongBao.query
    if nqt_loai_nd and nqt_nd_id:
        nqt_q = nqt_q.filter(
            (NqtThongBao.nqt_la_quang_ba == True) |
            ((NqtThongBao.nqt_loai_nguoi_nhan == nqt_loai_nd) &
             (NqtThongBao.nqt_ma_nguoi_nhan == nqt_nd_id))
        )
    else:
        nqt_q = nqt_q.filter_by(nqt_la_quang_ba=True)
    nqt_list = nqt_q.order_by(NqtThongBao.nqt_ngay_tao.desc()).limit(50).all()
    return nqt_ok([t.nqt_to_dict() for t in nqt_list])


@nqt_thong_bao_bp.route('/nqt-thong-bao', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_tao_thong_bao():
    nqt_data = request.get_json() or {}
    nqt_row = NqtThongBao(
        nqt_tieu_de=nqt_data.get('nqt_tieu_de', ''),
        nqt_noi_dung=nqt_data.get('nqt_noi_dung', ''),
        nqt_loai=nqt_data.get('nqt_loai', 'in_app'),
        nqt_la_quang_ba=nqt_data.get('nqt_la_quang_ba', False),
        nqt_ma_nguoi_nhan=nqt_data.get('nqt_ma_nguoi_nhan'),
        nqt_loai_nguoi_nhan=nqt_data.get('nqt_loai_nguoi_nhan'),
        nqt_du_lieu_them=nqt_data.get('nqt_du_lieu_them'),
    )
    db.session.add(nqt_row)
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict(), 'Gửi thông báo thành công', 201)


@nqt_thong_bao_bp.route('/nqt-thong-bao/<int:nqt_id>/nqt-doc', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_danh_dau_da_doc(nqt_id):
    nqt_row = NqtThongBao.query.get_or_404(nqt_id)
    nqt_row.nqt_la_da_doc = True
    db.session.commit()
    return nqt_ok(None, 'Đã đánh dấu là đã đọc')


@nqt_thong_bao_bp.route('/nqt-lich-gui-thong-bao', methods=['GET'])
@nqt_yeu_cau_dang_nhap
def nqt_lay_lich_gui():
    nqt_list = NqtLichGuiThongBao.query.all()
    return nqt_ok([l.nqt_to_dict() for l in nqt_list])


@nqt_thong_bao_bp.route('/nqt-lich-gui-thong-bao/<int:nqt_id>/nqt-bat-tat', methods=['PUT'])
@nqt_yeu_cau_dang_nhap
def nqt_bat_tat_lich_gui(nqt_id):
    nqt_row = NqtLichGuiThongBao.query.get_or_404(nqt_id)
    nqt_row.nqt_la_hoat_dong = not nqt_row.nqt_la_hoat_dong
    db.session.commit()
    return nqt_ok(nqt_row.nqt_to_dict())


@nqt_thong_bao_bp.route('/nqt-email/test', methods=['POST'])
@nqt_yeu_cau_dang_nhap
def nqt_gui_email_test():
    """Gửi email test để kiểm tra cấu hình SMTP."""
    from backend.app.services.nqt_dich_vu_cau_hinh import NqtDichVuCauHinh

    nqt_data = request.get_json() or {}
    nqt_email_nhan = nqt_data.get('nqt_email_nhan', '').strip()

    if not nqt_email_nhan:
        return nqt_loi('Vui lòng nhập email nhận')

    # Lấy cấu hình SMTP từ database
    nqt_smtp_host = NqtDichVuCauHinh.nqt_lay('smtp_host', nqt_mac_dinh='smtp.gmail.com')
    nqt_smtp_port = NqtDichVuCauHinh.nqt_lay('smtp_port', nqt_mac_dinh=587)
    nqt_smtp_bao_mat = NqtDichVuCauHinh.nqt_lay('smtp_bao_mat', nqt_mac_dinh='tls')
    nqt_smtp_email = NqtDichVuCauHinh.nqt_lay('smtp_email', nqt_mac_dinh='')
    nqt_smtp_mat_khau = NqtDichVuCauHinh.nqt_lay('smtp_mat_khau', nqt_mac_dinh='')
    nqt_email_gui_tu = NqtDichVuCauHinh.nqt_lay('email_gui_tu', nqt_mac_dinh=nqt_smtp_email)
    nqt_ten_nguoi_gui = NqtDichVuCauHinh.nqt_lay('ten_nguoi_gui_email', nqt_mac_dinh='NQT Gym')

    if not nqt_smtp_email or not nqt_smtp_mat_khau:
        return nqt_loi('Chưa cấu hình email đăng nhập SMTP và mật khẩu')

    try:
        # Tạo email
        nqt_msg = MIMEMultipart('alternative')
        nqt_msg['Subject'] = '✅ Test Email từ NQT Gym - Cấu hình SMTP thành công!'
        nqt_msg['From'] = f'{nqt_ten_nguoi_gui} <{nqt_email_gui_tu}>'
        nqt_msg['To'] = nqt_email_nhan

        nqt_html = f'''
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 30px; border-radius: 16px; text-align: center;">
                    <h1 style="color: white; margin: 0;">🎉 Test Email Thành Công!</h1>
                </div>
                <div style="background: #f8fafc; padding: 30px; border-radius: 16px; margin-top: 20px;">
                    <h2 style="color: #1e293b; margin-top: 0;">Cấu hình SMTP đã hoạt động</h2>
                    <p>Xin chào,</p>
                    <p>Đây là email test từ hệ thống <strong>NQT Gym Management</strong>.</p>
                    <p>Nếu bạn nhận được email này, nghĩa là cấu hình SMTP đã hoạt động đúng.</p>
                    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 20px 0;">
                    <p style="font-size: 14px; color: #64748b;">
                        <strong>Thông tin cấu hình:</strong><br>
                        SMTP Host: {nqt_smtp_host}<br>
                        SMTP Port: {nqt_smtp_port}<br>
                        Bảo mật: {nqt_smtp_bao_mat.upper()}<br>
                        Email gửi: {nqt_email_gui_tu}
                    </p>
                </div>
                <p style="text-align: center; color: #94a3b8; font-size: 12px; margin-top: 20px;">
                    &copy; 2026 NQT Gym Management System
                </p>
            </div>
        </body>
        </html>
        '''
        nqt_msg.attach(MIMEText(nqt_html, 'html', 'utf-8'))

        # Kết nối SMTP
        if nqt_smtp_bao_mat == 'ssl':
            nqt_server = smtplib.SMTP_SSL(nqt_smtp_host, int(nqt_smtp_port), timeout=30)
        else:
            nqt_server = smtplib.SMTP(nqt_smtp_host, int(nqt_smtp_port), timeout=30)
            if nqt_smtp_bao_mat == 'tls':
                nqt_server.starttls()

        nqt_server.login(nqt_smtp_email, nqt_smtp_mat_khau)
        nqt_server.sendmail(nqt_email_gui_tu, [nqt_email_nhan], nqt_msg.as_bytes())
        nqt_server.quit()

        return nqt_ok(None, f'Email test đã được gửi đến {nqt_email_nhan}')

    except smtplib.SMTPAuthenticationError:
        return nqt_loi('Sai email hoặc mật khẩu SMTP. Với Gmail, hãy dùng App Password.')
    except smtplib.SMTPConnectError:
        return nqt_loi(f'Không thể kết nối đến {nqt_smtp_host}:{nqt_smtp_port}')
    except Exception as e:
        return nqt_loi(f'Lỗi gửi email: {str(e)}')
