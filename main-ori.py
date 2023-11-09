import os
import pyrebase
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import auth, db, credentials, firestore

app = Flask(__name__)
app.secret_key = "foodlink"  # Replace with a strong secret key


# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate(
    "foodlink-f9689-firebase-adminsdk-fxylc-916b4eade2.json")
# Firebase setup (you should use your Firebase configuration)
config = {
    'apiKey': "AIzaSyDLo6oAxZQRS-6r2RkQJGdONQJax-5-2b8",
    'authDomain': "foodlink-f9689.firebaseapp.com",
    'projectId': "foodlink-f9689",
    'storageBucket': "foodlink-f9689.appspot.com",
    'messagingSenderId': "912138894281",
    'appId': "1:912138894281:web:514ff890b7ecb043ec0618",
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

# Firestore setup (you should use your Firestore configuration)
# Initialize Firestore
firebase_admin.initialize_app(cred)
db = firestore.client()

# Replace this with the code to initialize Firestore

# Home page


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')


@app.route('/sign-in')
def sign_in():
    return render_template('sign-in.html')

#########

# login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Add Firebase authentication logic to sign in the user
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user

            # After successful login, redirect to the appropriate page based on the user's role
            # You can add logic here to determine the role

            # Redirect to the user's home page
            return redirect(url_for('user_home'))
        except Exception as e:
            error_message = "Login failed. Please check your credentials and try again."

    return render_template('/login/login.html', error_message=error_message)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/register', methods=['POST'])
def register():
    # Implement user registration logic here using Firebase
    # Set user role based on the choice (user or donor)
    return redirect(url_for('login'))

###########
# test cloud firestore

# Define a function to get user data


def get_user_data(user_id):
    users_ref = firestore.client().collection('users')
    user_data = users_ref.document(user_id).get()
    return user_data.to_dict()


def get_all_users():
    users_ref = firestore.client().collection('users')
    all_users = []
    for user_doc in users_ref.stream():
        user_data = user_doc.to_dict()
        all_users.append(user_data)
    return all_users


@app.route('/users')
def users():
    all_users = get_all_users()
    return render_template('/admin/users.html', all_users=all_users)


@app.route('/profile/<user_id>')
def profile(user_id):
    user_data = get_user_data(user_id)
    return render_template('profile.html', user_data=user_data)


# # Define a route to display all users
# @app.route('/users')
# def display_users():
#     # Get a reference to the "users" node
#     users_ref = db.reference('users')

#     # Retrieve the list of users as a dictionary
#     users_data = users_ref.get()

#     # Check if there are users
#     if users_data:
#         # Create a list of user data dictionaries
#         users_list = []
#         for user_id, user_info in users_data.items():
#             users_list.append({
#                 'user_id': user_id,
#                 'name': user_info.get('name', 'N/A'),
#                 'email': user_info.get('email', 'N/A'),
#                 'gender': user_info.get('gender', 'N/A'),
#                 'role': user_info.get('role', 'N/A')
#             })

#         # Render the user data in an HTML table
#         return render_template('users.html', users_list=users_list)
#     else:
#         return "No users found in the database."

# to add user to cloud firestore


def create_user(user_data):
    users_ref = firestore.client().collection('users')
    new_user_ref = users_ref.add(user_data)
    return new_user_ref.id

###########


@app.route('/user-home')
def user_home():
    return render_template('/user/user-home.html')


@app.route('/donor-home')
def donor_home():
    return render_template('/donor/donor-home.html')


@app.route('/admin-home')
def admin_home():
    return render_template('/admin/admin-home.html')


@app.route('/dashboard')
def dashboard():
    # Implement dashboard logic based on the user role (admin)
    return render_template('/admin/dashboard.html')

# Other routes for specific pages like food statistics, user profile, etc.


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# if __name__ == '__main__':
#     app.run(debug=True)


app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), debug=True)
