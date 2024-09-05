from flask import Flask, render_template,request,redirect,url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password ="TechJita@97",
        database ="kota",

)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/order', methods = ['POST'])
def order():
    name = request.form['name']
    kota =request.form['kota']
    chips = request.form['chips']

    cursor = db.cursor()
    cursor.execute(
    "INSERT INTO orders(customer_name,kota_choice,chips_choice) VALUES(%s,%s,%s)", (name,kota,chips)
    )
    db.commit()
    cursor.close()
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    cursor = db.cursor()

    # Fetch customer name and order number from the database
    cursor.execute("SELECT id, customer_name FROM orders")
    orders = cursor.fetchall()

    cursor.close()  # Close the cursor
    # Pass the orders to the HTML template
    return render_template('order_number.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)