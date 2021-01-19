from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import Form
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customername = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    currentbalance = db.Column(db.Integer)
    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    def __repr__(self):
        return f"Customer('{self.customername}', '{self.email}', '{self.currentbalance}')"

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

    def __repr__(self):
        return f"Transaction('{self.amount}')"

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/transfer')
def transfer():
    return render_template('transfer.html')

@app.route('/transaction/<id>/',  methods=['GET', 'POST'])
def transaction(id):

    if request.method == 'POST':
        amount = request.form.get('amount')
        id = request.form.get('id')
        transaction = Transaction(amount = amount, customer_id = id)
        customer = Customer.query.get(id)
        customer.currentbalance += int(amount)
        db.session.add(customer)
        db.session.add(transaction)
        db.session.commit()
        return redirect(url_for('transfer'))
    return render_template('transaction.html', id=id)


@app.route('/javascript')
def javascript():
    return render_template('index.js')

@app.route('/search', methods=['GET', 'POST'])
def search():

    if request.method == 'POST':
        search = request.form.get('search')
        customers = Customer.query.filter_by(customername=search)
        customers = customers.order_by(Customer.customername).all()
    else:
        customers = Customer.query.all()


    return render_template('transfer.html', customers = customers)

if __name__ == '__main__':
    app.run(debug=True)
