from flask import Blueprint, render_template

donor_bp = Blueprint('donor', __name__, url_prefix='/donor')


@donor_bp.route('/')
def donor_home():
    return render_template('donor/donor-home.html')


@donor_bp.route('/donate')
def donate():
    return render_template('donor/donate.html')

@donor_bp.route('/contact-us')
def contact_us():
    return render_template('donor/contact-us.html')

# Define more routes specific to the donor module
