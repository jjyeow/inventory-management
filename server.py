import peeweedbevolve
from flask import Flask, render_template, request, flash, url_for, redirect
from models import db
from models import Store, Warehouse
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
@app.before_request 
def before_request(): 
    db.connect() 

@app.after_request
def after_request(response):
    db.close()
    return response

@app.cli.command()
def migrate():
    db.evolve(ignore_tables={'base_model'})

@app.route("/")
def index(): 
    return render_template('index.html')

@app.route("/shop")
def shop(): 
    return render_template('shop.html')

@app.route("/warehouse")
def warehouse():
    stores = Store.select()
    return render_template('warehouse.html', stores = stores)

@app.route("/warehouse_form", methods = ["POST"])
def warehouse_form():
    store_id = request.form.get('store_id')
    warehouse_location = request.form.get('location_name')
    # breakpoint()
    # store = Store.get_by_id(store_id) #if wanna pass Warehouse first argument as instance
    new_warehouse = Warehouse(store_id = store_id, location=warehouse_location)
    
    if new_warehouse.save():
        return redirect(url_for('warehouse'))
    
    else: 
        return render_template('warehouse.html', store_id = store_id, warehouse_location = warehouse_location) 
    
@app.route("/shop_form", methods = ["POST"])
def shop_form(): 
    store_name = request.form.get('store_name')
    store_details = Store(name=store_name)
    if store_details.save(): 
        flash('Store sucessfully saved!')
        return redirect(url_for('index'))
    else: 
        return render_template('shop.html', store_name = store_name)


if __name__ == '__main__':
    app.run() 