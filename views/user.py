from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/')
def user_home():
    return render_template('user/user-home.html')

@user_bp.route('/about')
def about():
    return render_template('user/about.html')

@user_bp.route('/contact-us')
def contact_us():
    return render_template('user/contact-us.html')

@user_bp.route('/get-food')
def get_food():
    return render_template('user/get-food.html')

@user_bp.route('/food-availability')
def food_availability():
    return render_template('user/food-availability.html')

# Define more routes specific to the user module
