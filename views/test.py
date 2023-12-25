# import firebase_admin
# from firebase_admin import credentials, firestore

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# def get_user_role(email):
#     users_ref = db.collection('users')
#     query = users_ref.where('email', '==', email).get()

#     if not query:
#         return 'User not found'
    
#     user = query[0].to_dict()
#     role = user.get('role', 'user')

#     return role

# # Testing the function
# test_email = 'ali@gmail.com'  # Replace with the email you want to test
# user_role = get_user_role(test_email)
# print(f"User role for {test_email}: {user_role}")
