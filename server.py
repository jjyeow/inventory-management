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

@app.route("/shop_index")
def shop_index():
    all_stores = Store.select() 
    # store_names = []
    # store_warehouse = []
    # store_details = []
    # store_id = []
    # for i in all_stores: 
    #     arr = [0]
    #     # store_names.append(i.name)
    #     stores_instance = Store.get_by_id(i.id)
    #     for j in stores_instance.warehouses: 
    #         arr.append(j)
    #     store_warehouse.append(len(arr)-1)

    # for j in range(len(store_names)):
    #     store_details.append({store_names[j]: store_warehouse[j]})

    # for k in all_stores:
    #     store_id.append(k.id)

    return render_template('view_all.html', all_stores = all_stores)

@app.route("/shop/delete", methods=["POST"])
def delete_shop(): 
    store_to_delete_id = request.form.get('store_to_delete')
    store_delete = Store.get_by_id(store_to_delete_id)
    Warehouse.delete().where(Warehouse.store_id == store_to_delete_id).execute()
    store_delete.delete_instance()
    

    return redirect(url_for("shop_index"))

@app.route("/shop/<store_id_view>",methods=["GET","POST"])
def view_shop(store_id_view):
    stores_id = Store.get_by_id(store_id_view)
    # if request.method == "GET":
    no_warehouse = [0]
    for i in stores_id.warehouses:
        no_warehouse.append(i)
        
    no_warehouse = len(no_warehouse) - 1
    return render_template('shop_view.html', stores_id = stores_id, no_warehouse = no_warehouse)
    # else:
    #     new_store_name = request.form.get('store_name_update')
    #     stores_id.name = new_store_name 
    #     if stores_id.save():
    #         return redirect(url_for("view_shop", store_id_view = store_id_view))

@app.route("/shop/<store_id_view>/update",methods=["POST"])
def edit_shop(store_id_view):
    stores_id = Store.get_by_id(store_id_view)
    new_store_name = request.form.get('store_name_update')
    stores_id.name = new_store_name 
    if stores_id.save():
        return redirect(url_for("view_shop", store_id_view = store_id_view))

    
# @app.route("/shop/<store_id_view>")
# def shop_updated(store_id_view):
#     stores_id = Store.get_by_id(store_id_view)
#     no_warehouse = [0]
#     for i in stores_id.warehouses:
#         no_warehouse.append(i)
           
#     no_warehouse = len(no_warehouse) - 1
    

#     return render_template('shop_view.html', stores_id = stores_id, no_warehouse = no_warehouse)

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