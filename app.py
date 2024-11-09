# Import necessary modules from Flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create an instance of the Flask class
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create an instance of the SQLAlchemy class
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Define the Login model for the database   
class Login(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Login('{self.name}', '{self.email}')"

# Define the Message model for the database
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Message('{self.name}', '{self.email}', '{self.message}')"

# Define the Booking model for the database
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('login.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    service = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Booking('{self.name}', '{self.email}', '{self.date}', '{self.time}', '{self.service}')"

# Define the Event model for the database
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}', '{self.time}')"


# Load the user
@login_manager.user_loader
def load_user(user_id):
    return Login.query.get(int(user_id))

# Define the routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Create a new message instance and add it to the database
        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].lower()
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if the passwords match
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')

        # Check if the email already exists in the Login table
        existing_user = Login.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error='Email is already registered')

        # Create a new login instance and add it to the database
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Hash the password
        new_login = Login(name=name, email=email, password=hashed_password)
        db.session.add(new_login)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']

        # Check if the email and password match an existing user in the Login table
        user = Login.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):  # Verify the hashed password
            login_user(user)
            if email == 'admin@coderdojo.com'.lower():  # Replace with your admin email
                return redirect(url_for('admin_dashboard'))  # Redirect to admin dashboard if admin
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    events = Event.query.all()
    if request.method == 'POST':
        event_id = request.form['event_id']
        event = Event.query.get(event_id)
        new_booking = Booking(
            user_id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            date=event.date,
            time=event.time,
            service=event.name
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('booking.html', events=events)

@app.route('/add_event', methods=['GET', 'POST'])
@login_required
def add_event():
    if current_user.email != 'admin@coderdojo.com':  # Ensure only admin can access
        return redirect(url_for('home'))
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        date_str = request.form['date']
        time_str = request.form['time']

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()

        new_event = Event(name=name, description=description, date=date, time=time)
        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_event.html')

@app.route('/manage_users')
@login_required
def manage_users():
    if not current_user.email == 'admin@coderdojo.com':
        return redirect(url_for('home'))
    users = Login.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/view_messages')
@login_required
def view_messages():
    if not current_user.email == 'admin@coderdojo.com':
        return redirect(url_for('home'))
    messages = Message.query.all()
    return render_template('view_messages.html', messages=messages)

@app.route('/view_bookings')
@login_required
def view_bookings():
    if not current_user.email == 'admin@coderdojo.com':
        return redirect(url_for('home'))
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/manage_events')
@login_required
def manage_events():
    if current_user.email != 'admin@coderdojo.com':  # Ensure only admin can access
        return redirect(url_for('home'))
    events = Event.query.all()
    return render_template('manage_events.html', events=events)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    if current_user.email != 'admin@coderdojo.com':  # Ensure only admin can delete events
        return redirect(url_for('home'))
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
    return redirect(url_for('manage_events'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    # You can add additional admin-specific checks here if needed
    return render_template('admin_dashboard.html')

# Run the app if this script is executed directly
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
