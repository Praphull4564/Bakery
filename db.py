import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Connect to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='praphull', 
            database='bakery',
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
    except Error as e:
        print(f"Error: {e}")
        return None
    return connection

def add_product(name, category, price, stock, description):
    """Add a product to the database."""
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
        INSERT INTO products (name, category, price, stock, description)
        VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (name, category, price, stock, description))
        connection.commit()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
    return True

def get_all_products():
    """Fetch all products from the database."""
    connection = get_db_connection()
    if connection is None:
        return []
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True for easier access to product fields
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    connection.close()
    return products

def add_predefined_products():
    """Add predefined products to the database if no products exist."""
    if not get_all_products():
        predefined_products = [
    ("White Bread", "Breads", 40.00, 50, "Soft and fluffy white bread, perfect for sandwiches."),
    ("Almond Puff", "Pastries", 45.00, 30, "Light and flaky pastry filled with almond cream."),
    ("Heavy Cream", "Dairy", 180.00, 40, "Rich heavy cream (250 ml), perfect for cooking and baking."),
    ("Mango Sorbet", "Ice Cream", 70.00, 200, "Refreshing mango sorbet made with real mangoes."),
    ("Whole Wheat Bread", "Breads", 45.00, 30, "Healthy whole wheat bread"),
    ("Sourdough Bread", "Breads", 60.00, 500, "Artisan sourdough bread with a crispy crust."),
    ("Croissant", "Pastries", 30.00, 100, "Flaky and buttery croissant."),
    ("Milk", "Dairy", 1000.00, 50, "Fresh milk (1 liter)"),
    ("Yogurt", "Dairy", 150.00, 80, "Creamy yogurt (500 grams)."),
    ("Chocolate Cake", "Cakes", 300.00, 25, "Rich chocolate cake with chocolate frosting."),
    ("Strawberry Ice Cream", "Ice Cream", 60.00, 450, "Creamy strawberry ice cream made with real strawberries."),
    ("Chocolate Chip Cookies", "Cookies", 25.00, 200, "Classic chocolate chip cookies, freshly baked."),
    ("Butterscotch Ice Cream", "Ice Cream", 50.00, 500, "Super Tasty Butterscotch Ice Cream"),
    ("Chocolate Cone", "Ice Cream", 50.00, 500, "Tasty Tasty Chooooocoooolateee!!!!!"),
    ("Rye Bread", "Breads", 60.00, 40, "Dense and flavorful rye bread."),
    ("Focaccia", "Breads", 70.00, 30, "Herb-infused Italian flatbread."),
    ("Danish Pastry", "Pastries", 35.00, 80, "Sweet pastry with cream cheese filling."),
    ("Eclair", "Pastries", 40.00, 60, "Cream-filled pastry topped with chocolate."),
    ("Butter", "Dairy", 200.00, 75, "Fresh unsalted butter (500 grams)."),
    ("Cheese", "Dairy", 250.00, 50, "Aged cheddar cheese (250 grams)."),
    ("Red Velvet Cake", "Cakes", 350.00, 20, "Classic red velvet cake with cream cheese frosting."),
    ("Oatmeal Raisin Cookies", "Cookies", 30.00, 150, "Chewy cookies with oats and raisins."),
    ("Peanut Butter Cookies", "Cookies", 30.00, 100, "Rich peanut butter cookies with a soft center."),
    ("Vanilla Ice Cream", "Ice Cream", 60.00, 400, "Creamy vanilla ice cream made with real vanilla."),
    ("Mint Chocolate Chip Ice Cream", "Ice Cream", 65.00, 350, "Refreshing mint ice cream with chocolate chips."),
    ("Ciabatta", "Breads", 50.00, 60, "Rustic Italian bread with a crispy crust."),
    ("Bagel", "Breads", 20.00, 90, "Classic bagel, perfect for breakfast."),
    ("Puff Pastry", "Pastries", 25.00, 100, "Flaky pastry ideal for savory and sweet dishes."),
    ("Tarts", "Pastries", 45.00, 50, "Delicious fruit tarts with a buttery crust."),
    ("Cream Cheese", "Dairy", 150.00, 70, "Smooth cream cheese (200 grams)."),
    ("Cheesecake", "Cakes", 400.00, 15, "Rich and creamy cheesecake with a graham cracker crust."),
    ("Snickerdoodle Cookies", "Cookies", 30.00, 120, "Soft cookies rolled in cinnamon sugar."),
    ("Cookies and Cream Ice Cream", "Ice Cream", 65.00, 300, "Creamy ice cream with chocolate cookie pieces."),
    ("Multigrain Bread", "Breads", 55.00, 40, "Nutritious multigrain bread packed with seeds."),
    ("Almond Croissant", "Pastries", 40.00, 80, "Croissant filled with almond cream and topped with sliced almonds."),
    ("Sour Cream", "Dairy", 120.00, 60, "Creamy sour cream (250 grams)."),
    ("Carrot Cake", "Cakes", 300.00, 20, "Moist carrot cake topped with cream cheese frosting."),
    ("Sugar Cookies", "Cookies", 25.00, 150, "Classic sugar cookies, lightly sweetened."),
    ("Coffee Ice Cream", "Ice Cream", 70.00, 250, "Rich coffee ice cream made with real coffee."),
    ("Garlic Bread", "Breads", 45.00, 80, "Delicious garlic-flavored bread."),
    ("Apple Strudel", "Pastries", 50.00, 40, "Traditional pastry filled with spiced apples."),
    ("Lemon Cake", "Cakes", 275.00, 25, "Zesty lemon cake with lemon frosting."),
    ("Dudh", "Dairy", 1500.00, 4000, "Tasty Tasty Milk")
]

        for product in predefined_products:
            add_product(*product)
        print("Predefined products added to the database")
    else:
        print("Products already exist in the database")
def delete_product(product_id):
    """Delete a product and its dependencies from the database."""
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # First delete from the cart
        cursor.execute("DELETE FROM cart WHERE product_id = %s", (product_id,))
        # Then delete from products
        cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        connection.commit()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
    return True

def update_product(product_id, price, stock, description):
    """Update product details in the database."""
    connection = get_db_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    query = """
        UPDATE products
        SET price = %s, stock = %s, description = %s
        WHERE product_id = %s
    """
    try:
        cursor.execute(query, (price, stock, description, product_id))
        connection.commit()
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        connection.close()
    return True