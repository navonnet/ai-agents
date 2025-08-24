import os
import pyodbc
from flask import Flask, render_template
from dotenv import load_dotenv
from flask import request
from models.customer import Customer
# Load .env
load_dotenv()

# Read connection string
connection_string = os.getenv("SQLSERVER_CONN")

# Flask app
app = Flask(__name__)

def mapTo(cursor, row, cls):
    columns = [column[0] for column in cursor.description]
    data = dict(zip(columns, row))
    return cls(**data)

@app.route("/")
def index():
    # Connect to SQL Server
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Fetch data
    cursor.execute("""SELECT 
                   TOP 10 CUstomer_id  as id, FIRST_NAME as firstName, LAST_NAME as lastName, 
                    EMAIL_ADDRESS as email FROM CUSTOMER""")
    
    rows = cursor.fetchall()

    customers = [mapTo(cursor, row, Customer) for row in rows]

    # Close
    cursor.close()
    conn.close()

    # Pass data to template
    return render_template("index.html", rows=customers)

@app.route("/customer/add",methods=["POST","GET"])
def addCustomer():
    if request.method == "POST":
        # Handle form submission to add a new customer
        pass
    
    return render_template("add_customer.html")

if __name__ == "__main__":
    app.run(debug=True)