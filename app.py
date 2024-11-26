from flask import Flask, render_template, redirect, url_for, request, session, g
from functools import wraps
from datetime import datetime
from db import add_product, get_all_products, add_predefined_products, delete_product, update_product
import mysql.connector

app = Flask(__name__)
app.secret_key = 'This is  a Yadav Bakery System'  

# Constants for admin credentials
ADMIN_USERNAME = "Golden"
ADMIN_PASSWORD = "4564"

# Decorator for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            print("User is not logged in, redirecting to login page.")
            return redirect(url_for('admin_login'))
        print("User is logged in.")
        return f(*args, **kwargs)
    return decorated_function


# Database connection management
@app.before_request
def connect_db():
    """Establishes a database connection at the start of each request."""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="praphull",
            database="bakery",
            auth_plugin='mysql_native_password'  
        )

@app.teardown_request
def close_db(exception):
    """Closes the database connection at the end of each request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True  
            print("Logged in successfully!")  
            return redirect(url_for('admin'))

    
    return render_template('adminlog.html', error=error)

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)  
    print("Logged out successfully.")  
    return redirect(url_for('home'))


@app.route('/admin')
@login_required
def admin():
    products = get_all_products()
    return render_template('admin.html', products=products)




@app.route('/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product_route(product_id):
    success = delete_product(product_id)
    return '', 204 if success else ('Error deleting product', 500)

@app.route('/update_product/<int:product_id>', methods=['POST'])
@login_required
def update_product_route(product_id):
    price = request.form.get("price")
    stock = request.form.get("stock")
    description = request.form.get("description")
    if update_product(product_id, price, stock, description):
        return redirect(url_for("admin"))
    else:
        return "Failed to update product", 500

@app.route('/add_product', methods=['POST'])
@login_required
def add_product_route():
    name = request.form.get('name')
    category = request.form.get('category')
    price = float(request.form.get('price'))
    stock = int(request.form.get('stock'))
    description = request.form.get('description')
    add_product(name, category, price, stock, description)
    return redirect(url_for('admin'))

@app.route('/menu')
def menu():
    products = get_all_products()
    categories = set(product['category'] for product in products)
    return render_template('menu.html', products=products, categories=categories)

@app.route('/process_order', methods=['POST'])
def process_order():
    try:
        # Get customer information
        customer_name = request.form['customer_name']
        customer_phone = request.form['customer_phone']
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor = None
        try:
            cursor = g.db.cursor(dictionary=True)
            cursor.execute("SELECT product_id, name, price FROM products")
            products = cursor.fetchall()
        finally:
            if cursor:
                cursor.close()

        total = 0.0
        receipt_details = []
        
        for product in products:
            product_id = product['product_id']
            quantity = int(request.form.get(f"quantity_{product_id}", 0))

            if quantity > 0:
                subtotal = float(product['price']) * quantity
                total += subtotal
                receipt_details.append({
                    "name": product['name'],
                    "quantity": quantity,
                    "price": float(product['price']),
                    "subtotal": subtotal
                })

        return render_template('receipt.html', receipt_details=receipt_details, total=total,
                               customer_name=customer_name, customer_phone=customer_phone,
                               date_time=date_time)
    except Exception as e:
        return str(e), 500

# Start the app
if __name__ == '__main__':
    add_predefined_products()  # Adds predefined products to the database if necessary
    app.run(debug=True)