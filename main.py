import os
from flask import Flask, render_template
from views.admin import admin_bp
from views.user import user_bp
from views.donor import donor_bp
from views.login import login_bp

app = Flask(__name__)
app.secret_key = "foodlink"  # Replace with a strong secret key

# Register the blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(donor_bp)
app.register_blueprint(login_bp)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

# if __name__ == '__main__':
#     app.run()


app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)), debug=True)
