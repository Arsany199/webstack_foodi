from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'
mail = Mail(app)

# Configuration for Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Replace with your mail server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'foodi'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_DEFAULT_SENDER'] = 'foodi@gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Sample data
menu_items = [
    {'name': 'Pizza', 'price': 10.00},
    {'name': 'Pasta', 'price': 8.00},
    {'name': 'Rice', 'price': 5.00}
]

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Here you would handle saving the user to your database
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Here you would handle user authentication
        return redirect(url_for('menu'))
    return render_template('login.html')

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    if request.method == 'POST':
        # Handle the order and send email
        items_ordered = request.form.getlist('items')
        total_price = sum(float(item.split(',')[1]) for item in items_ordered)
        send_order_email(items_ordered, total_price)
        flash('Order placed successfully. Check your email for details.')
        return redirect(url_for('menu'))
    return render_template('menu.html', items=menu_items)

def send_order_email(items, total):
    try:
        msg = Message('Order Confirmation', sender='arsanykamal30@gmail.com', recipients=['arsanykamal99@gmail.com'])
        msg.body = f'You have ordered: {items}\nTotal: ${total:.2f}'
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")
        flash('There was an issue sending the confirmation email. Please try again later.')

if __name__ == '__main__':
    app.run(debug=True)
