import streamlit as st
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="cdms"
)
cursor = conn.cursor()

st.set_page_config(page_title="CDMS", layout="wide")
st.title("📋 Customer Database Management System")

# Centering and fitting homepage image
col1, col2, col3 = st.columns([1, 4, 1])
with col2:
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS--GlCutMNTWYwqjnGtNlW-GlefaFgzKhRNQ&s", use_container_width=True)

st.header("WELCOME")
st.write("Efficient customer data handling is the backbone of any successful business.")
st.write("Customer Database Management System (CDMS) is a user-friendly, powerful, and secure tool designed to help you manage customer information seamlessly. ")
st.write("Built using SQL for database management, Python for backend processing, and Streamlit for an interactive web interface, this system simplifies customer data operations like storing, retrieving, updating, and analyzing—all in real-time.")

menu = st.sidebar.selectbox("Navigation", [
    "Search", "Customers", "Products", "Orders", "Payments", "Support Tickets"
])

def show_table(query, columns):
    cursor.execute(query)
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    st.dataframe(df, use_container_width=True)

if menu == "Search":
    st.subheader("🔍 Search")
    search_type = st.selectbox("Search By", [
        "Customer ID", "First Name", "Last Name", "Phone Number",
        "Product ID", "Payment ID", "Ticket Number"
    ])
    search_term = st.text_input("Enter Search Term")

    if search_term:
        if search_type == "Customer ID":
            query = f"SELECT * FROM Customers WHERE CustomerID = '{search_term}'"
            show_table(query, ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'Address', 'CreatedAt'])
        elif search_type == "First Name":
            query = f"SELECT * FROM Customers WHERE FirstName LIKE '%{search_term}%'"
            show_table(query, ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'Address', 'CreatedAt'])
        elif search_type == "Last Name":
            query = f"SELECT * FROM Customers WHERE LastName LIKE '%{search_term}%'"
            show_table(query, ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'Address', 'CreatedAt'])
        elif search_type == "Phone Number":
            query = f"SELECT * FROM Customers WHERE Phone LIKE '%{search_term}%'"
            show_table(query, ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'Address', 'CreatedAt'])
        elif search_type == "Product ID":
            query = f"SELECT * FROM Products WHERE ProductID = '{search_term}'"
            show_table(query, ['ProductID', 'ProductName', 'Description', 'Price', 'Stock', 'CreatedAt'])
        elif search_type == "Payment ID":
            query = f"SELECT * FROM Payments WHERE PaymentID = '{search_term}'"
            show_table(query, ['PaymentID', 'OrderID', 'PaymentDate', 'Amount', 'PaymentMethod'])
        elif search_type == "Ticket Number":
            query = f"SELECT * FROM SupportTickets WHERE TicketID = '{search_term}'"
            show_table(query, ['TicketID', 'CustomerID', 'Subject', 'Description', 'Status', 'CreatedAt'])

if menu == "Customers":
    st.subheader("📇 Customer List")
    show_table("SELECT * FROM Customers", ['CustomerID', 'FirstName', 'LastName', 'Email', 'Phone', 'Address', 'CreatedAt'])

    st.markdown("---")
    st.subheader("➕ Add or Delete Customer")
    option = st.radio("Choose Action", ["Add Customer", "Delete Customer"])

    if option == "Add Customer":
        col1, col2 = st.columns(2)
        with col1:
            cust_id = st.number_input("Customer ID", step=1)
            first = st.text_input("First Name")
            last = st.text_input("Last Name")
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
            address = st.text_area("Address")

        if st.button("Add Customer"):
            try:
                cursor.execute("""
                    INSERT INTO Customers (CustomerID, FirstName, LastName, Email, Phone, Address)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (cust_id, first, last, email, phone, address))
                conn.commit()
                st.success("Customer added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Delete Customer":
        del_id = st.number_input("Enter Customer ID to delete", step=1)
        if st.button("Delete Customer"):
            try:
                cursor.execute("DELETE FROM Customers WHERE CustomerID = %s", (del_id,))
                conn.commit()
                st.success("Customer deleted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if menu == "Products":
    st.subheader("📦 Product List")
    show_table("SELECT * FROM Products", ['ProductID', 'ProductName', 'Description', 'Price', 'Stock', 'CreatedAt'])

    st.markdown("---")
    st.subheader("➕ Add or Delete Product")
    option = st.radio("Choose Action", ["Add Product", "Delete Product"])

    if option == "Add Product":
        col1, col2 = st.columns(2)
        with col1:
            pid = st.text_input("Product ID")
            name = st.text_input("Product Name")
            desc = st.text_area("Description")
        with col2:
            price = st.number_input("Price", step=0.01)
            stock = st.number_input("Stock", step=1)

        if st.button("Add Product"):
            try:
                cursor.execute("""
                    INSERT INTO Products (ProductID, ProductName, Description, Price, Stock)
                    VALUES (%s, %s, %s, %s, %s)
                """, (pid, name, desc, price, stock))
                conn.commit()
                st.success("Product added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Delete Product":
        del_pid = st.text_input("Enter Product ID to delete")
        if st.button("Delete Product"):
            try:
                cursor.execute("DELETE FROM Products WHERE ProductID = %s", (del_pid,))
                conn.commit()
                st.success("Product deleted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if menu == "Orders":
    st.subheader("📦 Orders")
    show_table("SELECT * FROM Orders", ['OrderID', 'CustomerID', 'OrderDate', 'Status', 'TotalAmount'])

    st.markdown("---")
    st.subheader("➕ Add or Delete Order")
    option = st.radio("Choose Action", ["Add Order", "Delete Order"])

    if option == "Add Order":
        col1, col2 = st.columns(2)
        with col1:
            oid = st.number_input("Order ID", step=1)
            cid = st.number_input("Customer ID", step=1)
        with col2:
            status = st.selectbox("Status", ['Pending', 'Shipped', 'Delivered', 'Canceled'])
            total = st.number_input("Total Amount", step=0.01)

        if st.button("Add Order"):
            try:
                cursor.execute("""
                    INSERT INTO Orders (OrderID, CustomerID, Status, TotalAmount)
                    VALUES (%s, %s, %s, %s)
                """, (oid, cid, status, total))
                conn.commit()
                st.success("Order added successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Delete Order":
        del_oid = st.number_input("Enter Order ID to delete", step=1)
        if st.button("Delete Order"):
            try:
                cursor.execute("DELETE FROM Orders WHERE OrderID = %s", (del_oid,))
                conn.commit()
                st.success("Order deleted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if menu == "Payments":
    st.subheader("💳 Payments")
    show_table("SELECT * FROM Payments", ['PaymentID', 'OrderID', 'PaymentDate', 'Amount', 'PaymentMethod'])

    st.markdown("---")
    st.subheader("➕ Add or Delete Payment")
    option = st.radio("Choose Action", ["Add Payment", "Delete Payment"])

    if option == "Add Payment":
        oid = st.number_input("Order ID", step=1)
        amount = st.number_input("Amount", step=0.01)
        method = st.selectbox("Payment Method", ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'])

        if st.button("Add Payment"):
            try:
                cursor.execute("""
                    INSERT INTO Payments (OrderID, Amount, PaymentMethod)
                    VALUES (%s, %s, %s)
                """, (oid, amount, method))
                conn.commit()
                st.success("Payment recorded successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Delete Payment":
        del_pid = st.number_input("Enter Payment ID to delete", step=1)
        if st.button("Delete Payment"):
            try:
                cursor.execute("DELETE FROM Payments WHERE PaymentID = %s", (del_pid,))
                conn.commit()
                st.success("Payment deleted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

if menu == "Support Tickets":
    st.subheader("🎫 Support Tickets")
    show_table("SELECT * FROM SupportTickets", ['TicketID', 'CustomerID', 'Subject', 'Description', 'Status', 'CreatedAt'])

    st.markdown("---")
    st.subheader("➕ Add or Delete Ticket")
    option = st.radio("Choose Action", ["Add Ticket", "Delete Ticket"])

    if option == "Add Ticket":
        cust_id = st.number_input("Customer ID", step=1)
        subject = st.text_input("Subject")
        description = st.text_area("Description")
        status = st.selectbox("Status", ['Open', 'In Progress', 'Closed'])

        if st.button("Create Ticket"):
            try:
                cursor.execute("""
                    INSERT INTO SupportTickets (CustomerID, Subject, Description, Status)
                    VALUES (%s, %s, %s, %s)
                """, (cust_id, subject, description, status))
                conn.commit()
                st.success("Ticket submitted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

    elif option == "Delete Ticket":
        del_tid = st.number_input("Enter Ticket ID to delete", step=1)
        reason = st.text_area("Reason for deletion")
        if st.button("Delete Ticket"):
            if reason:
                try:
                    cursor.execute("DELETE FROM SupportTickets WHERE TicketID = %s", (del_tid,))
                    conn.commit()
                    st.success("Ticket deleted successfully!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("Please provide a reason for deletion.")
