# Import necessary modules
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore

# Flask application instance
app = Flask(__name__)

cred = credentials.Certificate("C:\\Users\\znaki\\OneDrive\\Desktop\\authenticationsystem.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define a route for the root URL
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    user_ref = db.collection('users').document()
    user_ref.set({
        'username': username,
        'email': email,
        'password': password
    })
    return "User registered successfully!"

if __name__ == '__main__':
    app.run(debug=True)


