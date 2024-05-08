# Import necessary modules
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore

# Flask application instance
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Initialize Firebase Admin SDK with service account credentials
cred = credentials.Certificate("C:\\Users\\AMINE\\Desktop\\authenticationsystem.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('login.html')

# Define a route for user login
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    # Query the Firestore database for the user with the provided email
    users_ref = db.collection('users')
    query = users_ref.where('email', '==', email).limit(1)
    users = query.stream()

    for user in users:
        user_data = user.to_dict()
        hashed_password = user_data.get('password')

        # Compare the hashed password with the provided password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            # Authentication successful, store user ID in session
            session['user_id'] = user.id
            return redirect(url_for('home'))

    # Authentication failed, redirect back to login page with a message
    return redirect(url_for('index', message='Invalid email or password'))

# Define a route for the home page
@app.route('/home')
def home():
    # Check if user is authenticated by checking if user ID is in session
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

# Define a route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Hash the password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Store user data in Firestore
        users_ref = db.collection('users')
        user_doc = users_ref.add({
            'username': username,
            'email': email,
            'password': hashed_password.decode('utf-8')  # Decode hashed password to store as string
        })

        # Set user ID in session after registration
        session['user_id'] = user_doc.id

        return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
