from flask import Flask, render_template, request, redirect, url_for
from models import db, Booking

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

        new_booking = Booking(name=name, email=email, phone=phone, destination=destination)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('success'))
    return render_template('booking.html')

@app.route('/success')
def success():
    return render_template('success.html')


# 👇 This part is required to actually run the app
if __name__ == '__main__':
    app.run(debug=True)
