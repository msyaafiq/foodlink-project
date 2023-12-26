from flask import Blueprint, render_template, request
import firebase_admin
from firebase_admin import credentials, db, initialize_app

user_bp = Blueprint('user', __name__, url_prefix='/user')

# Replace 'path/to/your/firebase/serviceAccountKey.json' with the actual path to your service account key file
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the Firebase Admin SDK with the credentials and the database URL
initialize_app(cred, {
               'databaseURL': 'https://foodlink-f9689-default-rtdb.asia-southeast1.firebasedatabase.app/'})

# Create a reference to the 'food-count' in the Realtime Database
food_count_ref = db.reference('food-count')

# Define a mapping of keys to full names
location_mapping = {
    'bukitJalil': 'National Stadium Bukit Jalil',
    'kualaLumpur': 'Kuala Lumpur City Centre (KLCC)',
    'putrajaya': 'Putrajaya',
}


@user_bp.route('/')
def user_home():
    return render_template('user/user-home.html')


@user_bp.route('/about')
def about():
    return render_template('user/about.html')


@user_bp.route('/user-profile')
def user_profile():
    return render_template('user/user-profile.html')

@user_bp.route('/contact-us')
def contact_us():
    return render_template('user/contact-us.html')


@user_bp.route('/get-food')
def get_food():
    return render_template('user/get-food.html')


@user_bp.route('/food-availability')
def food_availability():
    # return render_template('user/food-availability.html')
    selected_location_key = request.args.get('location', '')

    # Use the mapping to get the full name based on the key
    selected_location_full_name = location_mapping.get(
        selected_location_key, 'Unknown Location')

    return render_template('user/food-availability.html', selected_location=selected_location_full_name)

    # try:
    #     # Reference to the 'food-count' document in Firestore
    #     food_count_ref = db.collection('food-count').document('0')

    #     # Retrieve the food count from Firestore
    #     food_count_data = food_count_ref.get().to_dict()

    #     # Extract the 'count' field from the document
    #     food_count = food_count_data.get('count', 0)

    #     # Render the HTML template with the food count
    #     return render_template('user/food-availability.html', food_count=food_count)
    # except Exception as e:
    #     # Handle the exception (e.g., display an error page)
    #     print(f"Error fetching food count: {e}")
    #     return render_template('error.html', error_message="Failed to fetch food count")
