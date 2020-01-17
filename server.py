import peeweedbevolve
from flask import Flask, render_template, request, flash, url_for, redirect
from models import db
from models import Store
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

@app.route("/shop_form")
def shop_form(): 
    store_name = request.args.get('store_name')
    store_details = Store(name=store_name)
    if store_details.save(): 
        flash('Store sucessfully saved!')
        return redirect(url_for('index'))
    else: 
        return render_template('shop.html', store_name = store_name)


if __name__ == '__main__':
    app.run() 