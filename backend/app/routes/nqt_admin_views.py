from flask import Blueprint, render_template, request
from bs4 import BeautifulSoup
import re

nqt_admin_views_bp = Blueprint('g6_admin_views', __name__)

def nqt_render_admin_template(nqt_template_name):
    """
    Render template với hỗ trợ SPA navigation.
    Nếu request có header X-Partial: true, extract và trả về phần content + scripts.
    Ngược lại trả về full page với base layout.
    """
    nqt_is_partial = request.headers.get('X-Partial', '').lower() == 'true'

    if nqt_is_partial:
        # Render full template trước
        nqt_full_html = render_template(nqt_template_name)

        # Parse HTML và extract content
        nqt_soup = BeautifulSoup(nqt_full_html, 'html.parser')

        # Tìm content area (thường là div#nqt-content-area hoặc main content)
        nqt_content = nqt_soup.find(id='nqt-content-area')
        if not nqt_content:
            # Fallback: lấy phần trong body, bỏ sidebar và header
            nqt_main = nqt_soup.find('main')
            if nqt_main:
                # Bỏ header, chỉ lấy content div
                nqt_content_div = nqt_main.find('div', class_='p-8')
                if nqt_content_div:
                    nqt_content = nqt_content_div

        # Lấy styles + external scripts từ head (block head)
        nqt_head_extras = ''
        nqt_head = nqt_soup.find('head')
        if nqt_head:
            for nqt_tag in nqt_head.children:
                tag_name = getattr(nqt_tag, 'name', None)
                if tag_name == 'style':
                    nqt_head_extras += str(nqt_tag)
                elif tag_name == 'script' and nqt_tag.get('src'):
                    # External script từ {% block head %} — cần thiết cho các page (Chart.js, v.v.)
                    nqt_head_extras += str(nqt_tag)

        # Lấy scripts từ cuối body (block scripts) — bỏ qua scripts global của base (có data-nqt-base)
        nqt_scripts = ''
        nqt_body = nqt_soup.find('body')
        if nqt_body:
            for nqt_script in nqt_body.find_all('script'):
                if not nqt_script.get('data-nqt-base'):
                    nqt_scripts += str(nqt_script)

        # Trả về: head extras (styles + external scripts) + content + body scripts
        nqt_partial_html = nqt_head_extras
        if nqt_content:
            nqt_partial_html += str(nqt_content.decode_contents() if hasattr(nqt_content, 'decode_contents') else nqt_content)
        nqt_partial_html += nqt_scripts

        return nqt_partial_html

    return render_template(nqt_template_name)

@nqt_admin_views_bp.route('/admin/login')
def nqt_view_login():
    return render_template('admin/login.html')

@nqt_admin_views_bp.route('/admin/dashboard')
def nqt_view_dashboard():
    return nqt_render_admin_template('admin/dashboard.html')

@nqt_admin_views_bp.route('/admin/hoi-vien')
def nqt_view_hoi_vien():
    return nqt_render_admin_template('admin/hoi_vien.html')

@nqt_admin_views_bp.route('/admin/khach-hang')
def nqt_view_khach_hang():
    return nqt_render_admin_template('admin/khach_hang.html')

@nqt_admin_views_bp.route('/admin/goi-tap')
def nqt_view_goi_tap():
    return nqt_render_admin_template('admin/goi_tap.html')

@nqt_admin_views_bp.route('/admin/don-hang')
def nqt_view_don_hang():
    return nqt_render_admin_template('admin/don_hang.html')

@nqt_admin_views_bp.route('/admin/thanh-toan')
def nqt_view_thanh_toan():
    return nqt_render_admin_template('admin/thanh_toan.html')

@nqt_admin_views_bp.route('/admin/chi-nhanh')
def nqt_view_chi_nhanh():
    return nqt_render_admin_template('admin/chi_nhanh.html')

@nqt_admin_views_bp.route('/admin/nhan-vien')
def nqt_view_nhan_vien():
    return nqt_render_admin_template('admin/nhan_vien.html')

@nqt_admin_views_bp.route('/admin/cau-hinh')
def nqt_view_cau_hinh():
    return nqt_render_admin_template('admin/cau_hinh.html')
