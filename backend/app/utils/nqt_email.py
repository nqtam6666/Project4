import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.app.services.g6_dich_vu_cau_hinh import NqtDichVuCauHinh

def nqt_gui_email(email_nhan: str, tieu_de: str, html_noi_dung: str):
    """Gửi email sử dụng thông tin cấu hình SMTP trong cơ sở dữ liệu."""
    # Lấy cấu hình SMTP từ database
    nqt_smtp_host = NqtDichVuCauHinh.g6_lay('g6_smtp_host', nqt_mac_dinh='smtp.gmail.com')
    nqt_smtp_port = NqtDichVuCauHinh.g6_lay('g6_smtp_port', nqt_mac_dinh=587)
    nqt_smtp_bao_mat = NqtDichVuCauHinh.g6_lay('g6_smtp_bao_mat', nqt_mac_dinh='tls')
    nqt_smtp_email = NqtDichVuCauHinh.g6_lay('g6_smtp_email', nqt_mac_dinh='')
    nqt_smtp_mat_khau = NqtDichVuCauHinh.g6_lay('g6_smtp_mat_khau', nqt_mac_dinh='')
    nqt_email_gui_tu = NqtDichVuCauHinh.g6_lay('g6_email_gui_tu', nqt_mac_dinh=nqt_smtp_email)
    nqt_ten_nguoi_gui = NqtDichVuCauHinh.g6_lay('g6_ten_nguoi_gui_email', nqt_mac_dinh='G6 Gym')

    if not nqt_smtp_host:
        raise Exception('Chưa cấu hình Máy chủ SMTP (Host).')
    if not nqt_smtp_email or not nqt_smtp_mat_khau:
        raise Exception('Chưa cấu hình Email đăng nhập SMTP và mật khẩu.')

    # Tạo email
    nqt_msg = MIMEMultipart('alternative')
    nqt_msg['Subject'] = tieu_de
    nqt_msg['From'] = f'{nqt_ten_nguoi_gui} <{nqt_email_gui_tu}>'
    nqt_msg['To'] = email_nhan
    nqt_msg.attach(MIMEText(html_noi_dung, 'html', 'utf-8'))

    # Kết nối SMTP
    if nqt_smtp_bao_mat == 'ssl':
        nqt_server = smtplib.SMTP_SSL(nqt_smtp_host, int(nqt_smtp_port), timeout=30)
    else:
        nqt_server = smtplib.SMTP(nqt_smtp_host, int(nqt_smtp_port), timeout=30)
        if nqt_smtp_bao_mat == 'tls':
            nqt_server.starttls()

    nqt_server.login(nqt_smtp_email, nqt_smtp_mat_khau)
    nqt_server.sendmail(nqt_email_gui_tu, [email_nhan], nqt_msg.as_bytes())
    nqt_server.quit()
