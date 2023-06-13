import os 
from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

app = Flask(__name__)

bootstrap = Bootstrap(app)
env_config = os.getenv( "PROD_APP_SETTINGS" , "config.DevelopmentConfig" ) 
app.config.from_object(env_config) 

@app.route( "/" ) 
def  index (): 
  return  render_template('sitio/index.html')

@app.route('/registro_admin/')
def registro_admin():
    return render_template('sitio/registro_admin.html')

@app.route('/registro_usu/')
def registro_usu():
    return render_template('sitio/registro_usu.html')