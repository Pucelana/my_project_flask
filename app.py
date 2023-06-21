from flask import Flask, jsonify, request, render_template, send_file, url_for, redirect, session
from psycopg2 import connect, extras
from passlib.hash import bcrypt
from flask_bootstrap import Bootstrap
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os



UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)
app.secret_key = b',)U\xcf\x8bl\x7f\xf0\x9bB\x8dg'

host = 'dpg-ci8rgm5gkuvmfns8scu0-a.frankfurt-postgres.render.com'
port = 5432
dbname = 'postgresql_pgadmin_7giw'
user = 'postgresql_pgadmin_7giw_user'
password = 'APlGvw8Y1q7harEMM9FWUm37QzDApClU'

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

# Registro de Administradores
@app.route('/registro_admin/', methods=['GET','POST'])
def registro_admin():
    message = ''
    if request.method == 'POST' and 'nombre' in request.form and 'usuario' in request.form and 'email' in request.form and 'provincia' in request.form and 'categoria' in request.form and 'password' in request.form:
        nombre = request.form['nombre']
        primerApellido = request.form['primerApellido']
        segundoApellido = request.form['segundoApellido']
        admin = request.form['usuario']
        correo = request.form['email']
        provincia = request.form['provincia']
        categoria = request.form['categoria']
        password_adm = request.form['password']
        
        hashed_password = bcrypt.hash(password_adm)
         
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM administradores WHERE correo=%s", (correo,))
        account = cursor.fetchall()
        print(account)
        if account:
            message = 'Ya existe esta cuenta'
        elif not nombre or not primerApellido or not segundoApellido or not admin or not correo or not provincia or not categoria or not password_adm:
            message = 'Por favor, rellena los campos'
        else:
            cursor.execute("INSERT INTO administradores(nombre,primerapellido,segundoapellido,nombreusuario,correo,provincia,categoria,password) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(nombre,primerApellido,segundoApellido,admin,correo,provincia,categoria,hashed_password))
            conexion.commit()
            message = 'El registro se realizo con exito'
            return render_template('admin/login_admin.html', message=message)
    elif request.method == 'POST':
        message = 'Ocurrio algún problema'
    return render_template('sitio/registro_admin.html', message=message) 

# Login de Administradores
@app.route('/login_admin/', methods=['GET','POST'])
def login_admin():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        correo = request.form['email']
        entered_password = request.form['password']
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM administradores WHERE correo=%s",(correo,))
        user2 = cursor.fetchone()
        if user2 and bcrypt.verify(entered_password, user2[8]):
            session['loggedin'] = True
            session['id'] = user2[0]
            session['usuario'] = user2[4]
            session['email'] = user2[5]
            print('Contraseñas coinciden')
            return redirect(url_for('home_admin'))
        else:
            print('No coinciden las contraseñas')        
    elif request.method == 'POST':
        message = 'Por favor, rellene los campos' 
    return render_template('admin/login_admin.html')

@app.route('/registro_usu/')
def registro_usu():
    return render_template('sitio/registro_usu.html')
  
# Ruta para subir productos
@app.route('/home_admin')
def home_admin():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conexion.commit()
    cursor.close()
    conexion.close()
    return render_template('admin/home_admin.html', productos=productos)

@app.route('/home_admin/guardar', methods=['GET','POST'])
def home_admin_guardar():
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
    return redirect(url_for('home_admin'))

#Ruta para mostrar las imagenes
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(UPLOAD_FOLDER, imagen)
  
  
if __name__ == '__main__':
  app.run(debug=True)  
  