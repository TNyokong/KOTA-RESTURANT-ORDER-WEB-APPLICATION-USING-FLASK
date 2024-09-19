from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

# Establish a database connection
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="TechJita@97",
        database="kota"
    )
    print("Database connected successfully.")
except Error as e:
    print(f"Error connecting to MySQL: {e}")

# Generate a random order number
def generate_order_number():
    while True:
        order_number = random.randint(1000, 9999)  # Generate a 4-digit order number
        cursor = db.cursor()
        cursor.execute("SELECT order_number FROM orders WHERE order_number = %s", (order_number,))
        result = cursor.fetchone()
        cursor.close()
        if not result:  # If no such order number exists, return it
            return order_number

@app.route('/')
def index():
    return redirect(url_for('role_selection'))

@app.route('/role_selection')
def role_selection():
    return render_template('role_selection.html')

@app.route('/order_page')
def order_page():
    return render_template('order_form.html')

@app.route('/order', methods=['POST'])
def order():
    name = request.form['name']
    kota = request.form['kota']
    chips = request.form['chips']

    # Generate a random order number and calculate estimated wait time (e.g., 15 minutes)
    order_number = generate_order_number()
    wait_time = 15

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO orders (customer_name, kota_choice, chips_choice, order_number, wait_time, order_time) "
            "VALUES (%s, %s, %s, %s, %s, %s)", (name, kota, chips, order_number, wait_time, datetime.now())
        )
        db.commit()
        cursor.close()
    except Error as e:
        print(f"Error occurred: {e}")
    
    return render_template('order_success.html', order_number=order_number, wait_time=wait_time)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'Spane22':
            session['username'] = username
            return redirect(url_for('admin_orders'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/admin/orders')
def admin_orders():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    cursor = db.cursor()
    cursor.execute("SELECT id, customer_name, kota_choice, chips_choice, order_number, order_time, wait_time FROM orders ORDER BY order_time DESC")
    orders = cursor.fetchall()
    cursor.close()

    return render_template('admin_orders.html', orders=orders)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/admin/clear_orders', methods=['POST'])
def clear_orders():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM orders")
        db.commit()
        cursor.close()
        flash('All orders have been cleared successfully.')
    except Error as e:
        print(f"Error occurred: {e}")
        flash('Failed to clear orders.')

    return redirect(url_for('admin_orders'))


if __name__ == '__main__':
    app.run(debug=True)
