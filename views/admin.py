from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def admin_home():
    return render_template('admin/admin-dashboard.html')


@admin_bp.route('/report')
def report_page():
    return render_template('admin/report-page.html')


@admin_bp.route('/maintenance')
def maintenance():
    return render_template('admin/maintenance.html')


@admin_bp.route('/users-list')
def user_list_page():
    return render_template('admin/page-list-users.html')

@admin_bp.route('/add-users')   
def add_user_page():
    return render_template('admin/page-add-users.html')
