# Inventory Management System
This project is an Inventory Management System built using Django. It allows users to perform basic CRUD (Create, Read, Update, Delete) operations on inventory items. Additionally, users can generate reports to analyze inventory performance.

## How to Use
- Sign Up and Log In- Navigate to signup to create a new account. You'll receive an email for account activation.
  - User Roles
    - Admin: Admins have full CRUD (Create, Read, Update, Delete) access to all inventory items.
    - Regular User: Regular users can Create, Read, Update, and Delete only their own invetory items.They cannot manage inventory belonging to other users.
    - 
- Once logged in, you can:

### API Endpoints
- GET /inventory Returns a list of all inventories.
- GET /per_product/id Returns details of a single inventory item.
- POST /add_inventory' Creates a new inventory item.
- PUT /update/id: Updates an existing inventory item.
- DELETE /delete/id Deletes an inventory item.
- Reports:
  The dashboard at /dashboard will display visual reports, including sales trends, best-performing products, and inventory stock status.

### Requirements
To run this project, you need to have the following installed on your local machine:

1. Python 3.8+
2. Django 3.x or higher
3. Plotly (for data visualization)
4. django-pandas (for data processing)
5. Other dependencies: See requirements.txt


### technologies used
- Django
- SQLite
- HTML
- Bootstrap

## License and Copyright Information
Licensed under [MIT] ("https://github.com/T-erry/Inventory-management-system/blob/main/LICENSE")







