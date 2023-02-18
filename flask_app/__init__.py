from flask import Flask
from flask_bcrypt import Bcrypt
app = Flask(__name__)

app.secret_key = "cashistrash"

bcrypt = Bcrypt(app) 
DATABASE = "cash_flow_db" 