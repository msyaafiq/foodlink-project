from flask import Blueprint, render_template, request, redirect, url_for, flash
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Retrieve Firebase credentials
cred = credentials.Certificate("serviceAccountKey.json")

# Check if Firebase app is already initialized
if not firebase_admin._apps:
    # If not initialized, initialize Firebase app
    firebase_admin.initialize_app(
        cred, {'databaseURL': 'https://foodlink-f9689-default-rtdb.asia-southeast1.firebasedatabase.app/'})


def get_firebase_cred():
    return cred

# Initialize Firebase (use your Firebase configuration)
config = {
    'apiKey': "AIzaSyDLo6oAxZQRS-6r2RkQJGdONQJax-5-2b8",
    'authDomain': "foodlink-f9689.firebaseapp.com",
    'projectId': "foodlink-f9689",
    'storageBucket': "foodlink-f9689.appspot.com",
    'messagingSenderId': "912138894281",
    'appId': "1:912138894281:web:514ff890b7ecb043ec0618",
    'databaseURL': ""
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

login_bp = Blueprint('login', __name__, url_prefix='/login')


@login_bp.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = auth.sign_in_with_email_and_password(email, password)

            # Get the user's role from the database using the function
            user_role = get_user_role(email)

            if user_role == 'admin':
                print("User is an admin.")
                return redirect(url_for('admin.admin_home'))
            elif user_role == 'user':
                print("User is a user.")
                return redirect(url_for('user.user_home'))
            elif user_role == 'donor':
                print("User is a donor.")
                return redirect(url_for('donor.donor_home'))
            else:
                flash("Invalid role for the user.")
                return redirect(url_for('login.login_page'))
        except Exception as e:
            # Handle various login errors
            if "EMAIL_NOT_FOUND" in str(e):
                flash("Email not found. Please check your email and try again.")
                print("Email not found.")
            elif "INVALID_PASSWORD" in str(e):
                flash("Invalid password. Please check your password and try again.")
                print("Invalid password.")
            else:
                flash("Login failed. Please check your credentials and try again.")
                print("Login failed.")

    return render_template('login/login.html')


def get_user_role(email):
    firestore_db = firestore.client()  # Initialize Firestore client
    users_ref = firestore_db.collection("users")

    # Query Firestore to find the user with the provided email
    user_query = users_ref.where("email", "==", email).limit(1).stream()

    for user_doc in user_query:
        user_data = user_doc.to_dict()
        # Return the user's role or default to "user" if not found
        return user_data.get("role", "user")

    return "user"  # Return the default role if the user is not found


@login_bp.route('/forgot-password')
def forgot_password():
    return render_template('login/forgot.html')


@login_bp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        role = "user" if request.form.get("user-role") == "user" else "donor"

        try:
            # Register the user with Firebase Authentication
            user = auth.create_user_with_email_and_password(email, password)

            # Initialize Firestore
            firestore_db = firestore.client()

            # Define user data
            user_data = {
                "name": name,
                "email": email,
                "gender": gender,
                "role": role
            }

            # Store user data in Firestore with an auto-generated document ID
            users_ref = firestore_db.collection("users")
            new_user_ref = users_ref.add(user_data)

            flash("Registration successful! Please log in.")
            return redirect(url_for("login.login_page"))
        except Exception as e:
            flash(f"Registration failed: {str(e)}")

    return render_template('login/register.html')
