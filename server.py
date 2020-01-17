import peeweedbevolve
from flask import Flask, render_template, request
from models import db
from models import Store
app = Flask(__name__)

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
    store_name = request.args.get('store_name')
    store_details = Store(name=store_name)
    store_details.save()
    return render_template('index.html', store_name=store_name)

@app.route("/shop")
def shop(): 
    return render_template('shop.html')

if __name__ == '__main__':
    app.run() 