from flask import Blueprint, render_template
from reportlab.pdfgen import canvas
from io import BytesIO

from flask import Blueprint, render_template, make_response
import pdfkit
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

# Initialize Firestore client
firestore_db = firestore.Client()

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


@admin_bp.route('/generate-pdf')
def download_users_pdf():
    try:
        # Reference to the "User" collection, replace with your collection name
        users_ref = firestore_db.collection("User")

        # Query Firestore to get user data
        user_data = [user.to_dict() for user in users_ref.stream()]

        # Render the data in a PDF-friendly HTML template
        html = render_template('users_pdf_template.html', data=user_data)

        # Options for pdfkit
        options = {
            'quiet': ''
        }

        # Generate PDF from HTML
        pdf = pdfkit.from_string(html, False, options=options)

        # Create response with PDF
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=users_report.pdf'

        return response
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return render_template('error.html', error_message="Failed to generate PDF")