from flask import current_app, render_template_string
from flask_mail import Message
from backend.app import mail


class NqtDichVuEmail:
    """Service gửi email thông báo cho hội viên."""

    # Template email hết hạn gói tập
    _NQT_TEMPLATE_HET_HAN = """
    <!DOCTYPE html>
    <html lang="vi">
    <head><meta charset="UTF-8"><title>Thông báo hết hạn gói tập</title></head>
    <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
      <div style="max-width:600px; margin:auto; background:#fff; border-radius:8px; overflow:hidden;">
        <div style="background:#ef4444; padding:24px; text-align:center;">
          <h1 style="color:#fff; margin:0; font-size:22px;">⚠️ Gói tập sắp hết hạn</h1>
        </div>
        <div style="padding:24px;">
          <p>Xin chào <strong>{{ nqt_ho_ten }}</strong>,</p>
          <p>Chúng tôi xin thông báo gói tập của bạn sẽ hết hạn sau
             <strong style="color:#ef4444;">{{ nqt_so_ngay }} ngày</strong>
             (ngày <strong>{{ nqt_ngay_het_han }}</strong>).</p>
          <div style="background:#fef2f2; border-left:4px solid #ef4444;
                      padding:12px 16px; margin:20px 0; border-radius:4px;">
            <p style="margin:0;"><strong>Gói tập:</strong> {{ nqt_ten_goi }}</p>
            <p style="margin:4px 0 0;"><strong>Ngày hết hạn:</strong> {{ nqt_ngay_het_han }}</p>
          </div>
          <p>Hãy gia hạn sớm để không bị gián đoạn lịch tập luyện của bạn!</p>
          <div style="text-align:center; margin:28px 0;">
            <a href="{{ nqt_link_gia_han }}"
               style="background:#ef4444; color:#fff; padding:12px 28px;
                      border-radius:6px; text-decoration:none; font-weight:bold;">
              Gia hạn ngay
            </a>
          </div>
          <p style="color:#6b7280; font-size:13px;">
            Nếu bạn đã gia hạn, vui lòng bỏ qua email này.<br>
            Mọi thắc mắc liên hệ hotline hoặc đến trực tiếp phòng gym.
          </p>
        </div>
        <div style="background:#f9fafb; padding:16px; text-align:center; color:#9ca3af; font-size:12px;">
          © 2026 NQT Gym Management System
        </div>
      </div>
    </body>
    </html>
    """

    # Template email xác nhận đăng ký gói tập
    _NQT_TEMPLATE_XAC_NHAN_DANG_KY = """
    <!DOCTYPE html>
    <html lang="vi">
    <head><meta charset="UTF-8"><title>Xác nhận đăng ký gói tập</title></head>
    <body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">
      <div style="max-width:600px; margin:auto; background:#fff; border-radius:8px; overflow:hidden;">
        <div style="background:#22c55e; padding:24px; text-align:center;">
          <h1 style="color:#fff; margin:0; font-size:22px;">✅ Đăng ký gói tập thành công!</h1>
        </div>
        <div style="padding:24px;">
          <p>Xin chào <strong>{{ nqt_ho_ten }}</strong>,</p>
          <p>Chúc mừng! Bạn đã đăng ký gói tập thành công. Dưới đây là thông tin gói tập của bạn:</p>
          <div style="background:#f0fdf4; border-left:4px solid #22c55e;
                      padding:12px 16px; margin:20px 0; border-radius:4px;">
            <p style="margin:0;"><strong>Gói tập:</strong> {{ nqt_ten_goi }}</p>
            <p style="margin:4px 0 0;"><strong>Ngày bắt đầu:</strong> {{ nqt_ngay_bat_dau }}</p>
            <p style="margin:4px 0 0;"><strong>Ngày hết hạn:</strong> {{ nqt_ngay_het_han }}</p>
            <p style="margin:4px 0 0;"><strong>Giá:</strong> {{ nqt_gia_tien }}</p>
          </div>
          <p>Hãy mang theo QR code dưới đây để check-in tại phòng gym:</p>
          <div style="text-align:center; margin:20px 0;">
            <img src="{{ nqt_qr_url }}" alt="QR Check-in"
                 style="width:160px; height:160px; border:2px solid #e5e7eb; border-radius:8px;" />
          </div>
          <p style="color:#6b7280; font-size:13px;">
            Chúc bạn tập luyện hiệu quả! Mọi thắc mắc liên hệ phòng gym.
          </p>
        </div>
        <div style="background:#f9fafb; padding:16px; text-align:center; color:#9ca3af; font-size:12px;">
          © 2026 NQT Gym Management System
        </div>
      </div>
    </body>
    </html>
    """

    @staticmethod
    def nqt_gui_nhac_het_han(nqt_email: str, nqt_ho_ten: str, nqt_ten_goi: str,
                              nqt_ngay_het_han: str, nqt_so_ngay: int,
                              nqt_link_gia_han: str = '#') -> bool:
        """Gửi email nhắc hội viên gói tập sắp hết hạn."""
        try:
            nqt_noi_dung = render_template_string(
                NqtDichVuEmail._NQT_TEMPLATE_HET_HAN,
                nqt_ho_ten=nqt_ho_ten,
                nqt_ten_goi=nqt_ten_goi,
                nqt_ngay_het_han=nqt_ngay_het_han,
                nqt_so_ngay=nqt_so_ngay,
                nqt_link_gia_han=nqt_link_gia_han,
            )
            nqt_msg = Message(
                subject=f'[NQT Gym] Gói tập "{nqt_ten_goi}" sắp hết hạn sau {nqt_so_ngay} ngày',
                recipients=[nqt_email],
                html=nqt_noi_dung,
            )
            mail.send(nqt_msg)
            return True
        except Exception as nqt_loi:
            current_app.logger.error(f'[Email] Lỗi gửi mail hết hạn tới {nqt_email}: {nqt_loi}')
            return False

    @staticmethod
    def nqt_gui_xac_nhan_dang_ky(nqt_email: str, nqt_ho_ten: str, nqt_ten_goi: str,
                                   nqt_ngay_bat_dau: str, nqt_ngay_het_han: str,
                                   nqt_gia_tien: str, nqt_qr_url: str = '') -> bool:
        """Gửi email xác nhận đăng ký gói tập thành công."""
        try:
            nqt_noi_dung = render_template_string(
                NqtDichVuEmail._NQT_TEMPLATE_XAC_NHAN_DANG_KY,
                nqt_ho_ten=nqt_ho_ten,
                nqt_ten_goi=nqt_ten_goi,
                nqt_ngay_bat_dau=nqt_ngay_bat_dau,
                nqt_ngay_het_han=nqt_ngay_het_han,
                nqt_gia_tien=nqt_gia_tien,
                nqt_qr_url=nqt_qr_url,
            )
            nqt_msg = Message(
                subject=f'[NQT Gym] Đăng ký gói "{nqt_ten_goi}" thành công!',
                recipients=[nqt_email],
                html=nqt_noi_dung,
            )
            mail.send(nqt_msg)
            return True
        except Exception as nqt_loi:
            current_app.logger.error(f'[Email] Lỗi gửi mail xác nhận tới {nqt_email}: {nqt_loi}')
            return False

    @staticmethod
    def nqt_gui_thong_bao_chung(nqt_email: str, nqt_tieu_de: str,
                                 nqt_noi_dung_text: str) -> bool:
        """Gửi email thông báo chung dạng text."""
        try:
            nqt_msg = Message(
                subject=f'[NQT Gym] {nqt_tieu_de}',
                recipients=[nqt_email],
                body=nqt_noi_dung_text,
            )
            mail.send(nqt_msg)
            return True
        except Exception as nqt_loi:
            current_app.logger.error(f'[Email] Lỗi gửi mail thông báo tới {nqt_email}: {nqt_loi}')
            return False
