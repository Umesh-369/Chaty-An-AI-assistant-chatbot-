import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from google import genai
import firebase_admin
from firebase_admin import credentials, firestore
from werkzeug.security import generate_password_hash, check_password_hash

# --- FIREBASE SETUP ---
try:
    if not firebase_admin._apps:
        # User needs to place their service account JSON as 'firebase-key.json'
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Firebase Init Warning: {e}. Ensure firebase-key.json is present for database functionality.")
    if not firebase_admin._apps:
        firebase_admin.initialize_app()

db = firestore.client()

client = genai.Client(api_key="YOUR GEMINI API KEY")
app = Flask(__name__)
app.secret_key = 'Your key'

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        
        if not email or not password:
            return render_template("signup.html", error="Email and password are required.")
        
        # Email Duplication Prevention
        try:
            user_ref = db.collection('users').document(email).get()
            if user_ref.exists:
                return render_template("signup.html", error="Email already registered.")
        except Exception as e:
             return render_template("signup.html", error="Database connection error. Please ensure Firebase is configured.")
        
        # Password Hashing
        hashed_pw = generate_password_hash(password)
        db.collection('users').document(email).set({
            'name': name,
            'email': email,
            'password': hashed_pw
        })
        
        session['user'] = {'email': email, 'name': name}
        return redirect(url_for('dashboard'))
        
    return render_template("signup.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            user_doc = db.collection('users').document(email).get()
            if not user_doc.exists:
                return render_template("login.html", error="invalid email or password")
            
            user_data = user_doc.to_dict()
            if check_password_hash(user_data['password'], password):
                session['user'] = {'email': email, 'name': user_data.get('name', 'Operator')}
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="invalid email or password")
        except Exception as e:
            return render_template("login.html", error="Database connection error.")
            
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("dashboard.html", user=session['user'])

@app.route('/chat_app')
def chat_app():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if 'user' not in session:
        return jsonify({"reply": "Unauthorized. Please login again."}), 401
    try:
        prompt = request.json["message"]
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"reply": f"Error generating response. Please try again."}), 200

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":

    app.run(port=8080, debug=True)
