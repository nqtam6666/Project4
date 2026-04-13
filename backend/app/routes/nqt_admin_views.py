from flask import Blueprint, render_template

nqt_admin_views_bp = Blueprint('nqt_admin_views', __name__)

@nqt_admin_views_bp.route('/admin/login')
def nqt_view_login():
    return render_template('admin/login.html')

@nqt_admin_views_bp.route('/admin/dashboard')
def nqt_view_dashboard():
    return render_template('admin/dashboard.html')

@nqt_admin_views_bp.route('/admin/hoi-vien')
def nqt_view_hoi_vien():
    return render_template('admin/hoi_vien.html')

@nqt_admin_views_bp.route('/admin/goi-tap')
def nqt_view_goi_tap():
    return render_template('admin/goi_tap.html')
