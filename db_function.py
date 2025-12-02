import mysql.connector

def connect_to_db():
    try:
        return mysql.connector.connect(
                host='localhost',
                username='root',
                password='Rahul@0628',
                database='project'
            )

    except:
        return "Something error occured..."
def get_basic_info(cursor):
    queries = {
        "Total Suppliers": "SELECT COUNT(*) AS count FROM suppliers",

        "Total Products": "SELECT COUNT(*) AS count FROM products",

        "Total Categories Dealing": "SELECT COUNT(DISTINCT category) AS count FROM products",

        "Total Sale Value (Last 3 Months)": """
        SELECT ROUND(SUM(ABS(se.change_quantity) * p.price), 2) AS total_sale
        FROM stock_entries se
        JOIN products p ON se.product_id = p.product_id
        WHERE se.change_type = 'Sale'
        AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Total Restock Value (Last 3 Months)": """
        SELECT ROUND(SUM(se.change_quantity * p.price), 2) AS total_restock
        FROM stock_entries se
        JOIN products p ON se.product_id = p.product_id
        WHERE se.change_type = 'Restock'
        AND se.entry_date >= (
        SELECT DATE_SUB(MAX(entry_date), INTERVAL 3 MONTH) FROM stock_entries)
        """,

        "Below Reorder & No Pending Reorders": """
        SELECT COUNT(*) AS below_reorder
        FROM products p
        WHERE p.stock_quantity < p.reorder_level
        AND p.product_id NOT IN (
        SELECT DISTINCT product_id FROM reorders WHERE status = 'Pending')
        """
        }

    result={}
    for label,query in queries.items():
        cursor.execute(query)
        data=cursor.fetchone()
        result[label]=list(data.values())[0]
    return result

def get_editional_table(cursor):
    queries = {
        "Suppliers Contact Details": "SELECT supplier_name, contact_name, email, phone FROM suppliers",

        "Products with Supplier and Stock": """
            SELECT 
                p.product_name,
                s.supplier_name,
                p.stock_quantity,
                p.reorder_level
            FROM products p
            JOIN suppliers s ON p.supplier_id = s.supplier_id
            ORDER BY p.product_name ASC
        """,

        "Products Needing Reorder": """
            SELECT product_name, stock_quantity, reorder_level
            FROM products
            WHERE stock_quantity <= reorder_level
        """
    }

    tables = {}
    for label, query in queries.items():
        cursor.execute(query)
        tables[label] = cursor.fetchall()
    return tables


def add_new_product(cursor,db,p_name,p_catgory,p_price,p_stock,p_reorder,p_supplier):
    procedure_call="call add_new_product(%s,%s,%s,%s,%s,%s)"
    parameter=(p_name,p_catgory,p_price,p_stock,p_reorder,p_supplier)
    cursor.execute(procedure_call,parameter)
    db.commit()

def get_categories(cursor):
    cursor.execute("SELECT DISTINCT category FROM products")
    data=cursor.fetchall()
    return [row['category'] for row in data]

def get_supplier(cursor):
    cursor.execute("SELECT supplier_id,supplier_name FROM suppliers")
    return cursor.fetchall()
def get_product(cursor):
    cursor.execute("""select product_id,product_name from products
    group by product_id,product_name""")
    return cursor.fetchall()

def get_product_history(cursor,input_product_id):
    query="SELECT * FROM product_history WHERE product_id=%s order by record_date desc"
    parameter=[input_product_id]
    cursor.execute(query,parameter)
    return cursor.fetchall()

def product_reorder(cursor,db,product_id,reorder_quantity):
    query="""INSERT INTO reorders(reorder_id,product_id,reorder_quantity,reorder_date,status)
             SELECT max(reorder_id)+1,%s,%s,curdate(),"Ordered" from reorders"""
    parameter=(product_id,reorder_quantity)
    cursor.execute(query,parameter)
    db.commit()
def get_pending_order(cursor):
    cursor.execute("""
    select t1.reorder_id,t2.product_name from reorders t1
                   join products t2
                   on t1.product_id=t2.product_id
                   where status='Pending'
    """)
    return cursor.fetchall()

def receive_order(cursor,db,input_recieve_id):
    procedurea_call="call receive_order(%s)"
    parameter=[input_recieve_id]
    cursor.execute(procedurea_call,parameter)
    db.commit()