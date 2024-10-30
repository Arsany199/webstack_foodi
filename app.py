from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = Mail(app)
db = SQLAlchemy(app)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'foody5066@gmail.com'
app.config['MAIL_PASSWORD'] = 'pass.123'
app.config['MAIL_DEFAULT_SENDER'] = 'foody5066@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

mail = Mail(app)

# Sample data
menu_items = [
        {'name': 'Pizza', 'price': 10.00, 'image_url': 'https://images.pexels.com/photos/708587/pexels-photo-708587.jpeg?auto=compress&cs=tinysrgb&w=600'},
        {'name': 'Pasta', 'price': 8.00, 'image_url': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=600'},
        {'name': 'Rice', 'price': 5.00, 'image_url': 'https://images.pexels.com/photos/723198/pexels-photo-723198.jpeg?auto=compress&cs=tinysrgb&w=600'},
        {'name': 'shawerma', 'price': 7.00, 'image_url': 'https://images.pexels.com/photos/5779364/pexels-photo-5779364.jpeg?auto=compress&cs=tinysrgb&w=600'}
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        # Store user in the dictionary (use a database in production)
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please log in.')
            return redirect(url_for('login'))

        # Create new user
        new_user = User(username=username, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['email'] = email  # Store email in session
            return redirect(url_for('menu'))
        else:
            flash('Invalid email or password. Please try again.')

    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if 'email' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle the order and send email
        items_ordered = request.form.getlist('items')
        total_price = sum(float(item.split(',')[1]) for item in items_ordered)
        if items_ordered:
            send_order_email(items_ordered, total_price)
            flash('Order placed successfully. Check your email for details.')
        else:
            flash('No items selected for order.')
        return redirect(url_for('menu'))
    return render_template('menu.html', items=menu_items)

def send_order_email(items, total):
    try:
        item_list = '\n'.join(items)
        msg = Message('Order Confirmation', recipients=[session['email']])
        msg.body = f'You have ordered:\n{item_list}\nTotal: ${total:.2f}'
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash('There was an issue sending the confirmation email. Please try again later.')

if __name__ == '__main__':
    app.run(debug=True)
