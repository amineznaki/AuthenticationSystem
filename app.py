# Import necessary modules
import bcrypt
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

# Flask application instance
app = Flask(__name__)

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate("C:\\Users\\znaki\\OneDrive\\Desktop\\authenticationsystem.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')

# Define a route for user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Store user data in Firestore
    users_ref = db.collection('users')
    users_ref.add({
        'username': username,
        'email': email,
        'password': hashed_password.decode('utf-8')  # Decode hashed password to store as string
    })

    return "User registered successfully!"

if __name__ == '__main__':
    app.run(debug=True)
