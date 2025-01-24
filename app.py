from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'igkcqduteudlzsrr'

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'bennysonsamuel567@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'igkcqduteudlzsrr'  # Your email password or app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'bennysonsamuel567@gmail.com'

mail = Mail(app)


# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Change if needed
db = client['contact_form_db']  # Database name
collection = db['submissions']  # Collection name


@app.route('/')
def index():
    return render_template('index.html')  

@app.route('/contact', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        msg = Message(
            subject=f"New Message from {name}",
            sender=email,
            recipients=['lightningthunder84@gmail.com'],  # Your email to receive the form submissions
            body=f"Name: {name}\nEmail: {email}\nMessage:\n{message}"
        )
        try:
            mail.send(msg)
        except Exception as e:
            flash(f"Error sending email: {e}", "danger")
            return redirect(url_for('home'))

        # Store data in MongoDB
        form_data = {
            'name': name,
            'email': email,
            'message': message
        }

        try:
            collection.insert_one(form_data)
            flash("Your message has been sent successfully and stored in the database!", "success")
        except Exception as e:
            flash(f"Error saving data to database: {e}", "danger")
        
        # Send greeting email to the user (the email submitted in the form)
        greeting_msg = Message(
            subject="Thank you for contacting us!",
            sender="bennysonsamuel567@gmail.com",  # Your email
            recipients=[email],  # The email submitted in the form
            body=f"Hello {name},\n\nThank you for your valuable feedback. We have received your message and will get back to you soon.\n\nBest regards,\nAccelero Realm"
        )
        try:
            mail.send(greeting_msg)
        except Exception as e:
            flash(f"Error sending greeting email: {e}", "danger")

        return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/contact')
def contact():
    return render_template('contact.html')  

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)