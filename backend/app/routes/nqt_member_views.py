from flask import Blueprint, render_template, request
from bs4 import BeautifulSoup

nqt_member_views_bp = Blueprint('nqt_member_views', __name__)


def nqt_render_member_template(nqt_template_name):
    nqt_is_partial = request.headers.get('X-Partial', '').lower() == 'true'
    if not nqt_is_partial:
        return render_template(nqt_template_name)

    nqt_full_html = render_template(nqt_template_name)
    nqt_soup = BeautifulSoup(nqt_full_html, 'html.parser')

    nqt_content = nqt_soup.find(id='nqt-member-content')
    nqt_head_extras = ''
    nqt_head = nqt_soup.find('head')
    if nqt_head:
        for tag in nqt_head.children:
            tag_name = getattr(tag, 'name', None)
            if tag_name == 'style':
                nqt_head_extras += str(tag)
            elif tag_name == 'script' and tag.get('src'):
                nqt_head_extras += str(tag)

    nqt_scripts = ''
    nqt_body = nqt_soup.find('body')
    if nqt_body:
        for nqt_script in nqt_body.find_all('script'):
            if not nqt_script.get('data-nqt-base'):
                nqt_scripts += str(nqt_script)

    nqt_partial_html = nqt_head_extras
    if nqt_content:
        nqt_partial_html += nqt_content.decode_contents()
    nqt_partial_html += nqt_scripts
    return nqt_partial_html


# ── Page routes ───────────────────────────────────────────────────────────────

@nqt_member_views_bp.route('/')
def nqt_trang_chu():
    return render_template('landing.html')


@nqt_member_views_bp.route('/member/login')
def nqt_member_login():
    return render_template('member/login.html')


@nqt_member_views_bp.route('/member/dashboard')
def nqt_member_dashboard():
    return nqt_render_member_template('member/dashboard.html')


@nqt_member_views_bp.route('/member/ho-so')
def nqt_member_ho_so():
    return nqt_render_member_template('member/ho_so.html')
