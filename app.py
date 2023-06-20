from flask import Flask, jsonify, request, render_template, send_file, url_for, redirect
from psycopg2 import connect, extras
from flask_bootstrap import Bootstrap
"""from cryptography.fernet import Fernet # Encriptar la contraseña"""
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)

host = 'dpg-ci8rgm5gkuvmfns8scu0-a.frankfurt-postgres.render.com'
port = 5432
dbname = 'postgresql_pgadmin_7giw'
user = 'postgresql_pgadmin_7giw_user'
password = 'APlGvw8Y1q7harEMM9FWUm37QzDApClU'

"""key = Fernet.generate_key()"""
bootstrap = Bootstrap(app)
env_config = os.getenv( "PROD_APP_SETTINGS" , "config.DevelopmentConfig" ) 
app.config.from_object(env_config) 



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
  
# Ruta para subir productos
@app.route('/productos/')
def productos():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conexion.commit()
    cursor.close()
    conexion.close()
    return render_template('admin/home_admin.html', productos=productos)

@app.route('/productos/guardar', methods=['GET','POST'])
def productos_guardar():
    producto = request.form['producto']
    imagen = request.files['imagen']
    url = request.form['url']
    genero = request.form['genero']
    descripcion = request.form['descrip']
    if imagen and allowed_file(imagen.filename):
        filename = secure_filename(imagen.filename)
        imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        conexion = get_connection()
        cursor = conexion.cursor(cursor_factory=extras.RealDictCursor)
        cursor.execute("INSERT INTO productos(producto,imagen,url,genero,descripcion) VALUES(%s,%s,%s,%s,%s)",(producto, filename, url, genero, descripcion))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for('productos'))

#Ruta para mostrar las imagenes
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(UPLOAD_FOLDER, imagen)
  
  
if __name__ == '__main__':
  app.run(debug=True)  