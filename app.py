from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "mysecretkey123"  # Needed for sessions

db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        destination = request.form['destination']
        date = request.form['date']

        new_booking = Booking(name=name, email=email, phone=phone, destination=destination, date=date)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('success'))
    return render_template('booking.html')

@app.route('/success')
def success():
    return render_template('success.html')


# 👇 Admin login route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hardcoded credentials for now
        if username == "admin" and password == "password123":
            session['admin'] = True
            flash("Login successful!", "success")
            return redirect(url_for('view_bookings'))
        else:
            error = "Invalid username or password"

    return render_template('admin_login.html', error=error)


# 👇 View bookings (protected)
@app.route('/admin/bookings')
def view_bookings():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    bookings = Booking.query.all()
    return render_template('view_bookings.html', bookings=bookings)


# 👇 Admin logout
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run(debug=True)
