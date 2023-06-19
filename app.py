from flask import Flask, jsonify, request, render_template, send_file, url_for, redirect
from psycopg2 import connect, extras
from flask_bootstrap import Bootstrap
from cryptography.fernet import Fernet # Encriptar la contraseña
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)

key = Fernet.generate_key()
bootstrap = Bootstrap(app)
env_config = os.getenv( "PROD_APP_SETTINGS" , "config.DevelopmentConfig" ) 
app.config.from_object(env_config) 

host = 'dpg-ci88o6p8g3n3vm436nf0-a'
port = 5432
dbname = 'my_project_db_lg3e'
user = 'my_project_db_lg3e_user'
password = 'HppJoMDM3FO0XxIM10riHCXcVgw8O70y'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower()in ALLOWED_EXTENSIONS

# Creamos la conexion a la base de datos
def get_connection():
    conexion = connect(host=host, port=port, dbname=dbname, user=user, password=password)
    return conexion

@app.route( "/" ) 
def  index (): 
  return  render_template('sitio/index.html')

@app.route('/registro_admin/')
def registro_admin():
    return render_template('sitio/registro_admin.html')

@app.route('/registro_usu/')
def registro_usu():
    return render_template('sitio/registro_usu.html')