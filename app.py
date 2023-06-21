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
def  home_sitio(): 
  return  render_template('sitio/home_sitio.html')

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
            session['admin'] = user2[4]
            session['email'] = user2[5]
            print('Contraseñas coinciden')
            return redirect(url_for('home_admin'))
        else:
            print('No coinciden las contraseñas')        
    elif request.method == 'POST':
        message = 'Por favor, rellene los campos' 
    return render_template('admin/login_admin.html')

# Registro de usuarios
@app.route('/registro_usu/', methods=['GET','POST'])
def registro_usu():
    message = ''
    if request.method == 'POST' and 'nombre' in request.form and 'usuario' in request.form and 'email' in request.form and 'password' in request.form:
        nombre = request.form['nombre']
        usuario = request.form['usuario']
        correo = request.form['email']
        password_usu = request.form['password']
        
        hashed_password = bcrypt.hash(password_usu)
         
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo,))
        account = cursor.fetchall()
        print(account)
        if account:
            message = 'Ya existe esta cuenta'
        elif not nombre or not usuario or not correo or not password_usu:
            message = 'Por favor, rellena los campos'
        else:
            cursor.execute("INSERT INTO usuarios(nombre,usuario,correo,password) VALUES(%s,%s,%s,%s)",(nombre,usuario,correo,hashed_password))
            conexion.commit()
            message = 'El registro se realizo con exito'
            return render_template('usu/login_usu.html', message=message)
    elif request.method == 'POST':
        message = 'Ocurrio algún problema'
    return render_template('sitio/registro_usu.html')

# Login de usuarios
@app.route('/login_usu/', methods=['GET','POST'])
def login_usu():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        correo = request.form['email']
        entered_password = request.form['password']
        conexion = get_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE correo=%s",(correo,))
        user2 = cursor.fetchone()
        if user2 and bcrypt.verify(entered_password, user2[4]):
            session['loggedin'] = True
            session['id'] = user2[0]
            session['usuario'] = user2[2]
            session['email'] = user2[3]
            print('Contraseñas coinciden')
            return redirect(url_for('usu_galeria'))
        else:
            print('No coinciden las contraseñas')        
    elif request.method == 'POST':
        message = 'Por favor, rellene los campos' 
    return render_template('usu/login_usu.html')
  
# Ruta para subir productos
@app.route('/admin')
def admin():
    conexion = get_connection()
    cursor = conexion.cursor(cursor_factory=extras.RealDictCursor)
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    conexion.commit()
    cursor.close()
    conexion.close()
    return render_template('admin/admin.html', productos=productos)

# Ruta para guardar los productos en la tabla
@app.route('/admin/guardar', methods=['GET','POST'])
def admin_guardar():
    admin = session['admin']
    email = session['email']
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
        cursor.execute("INSERT INTO productos(email,administrador,producto,imagen,url,genero,descripcion) VALUES(%s,%s,%s,%s,%s,%s,%s)",(email,admin,producto, filename, url, genero, descripcion))
        conexion.commit()
        cursor.close()
        conexion.close()
    return redirect(url_for('admin'))

#Ruta para mostrar las imagenes
@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(UPLOAD_FOLDER, imagen)

# Ruta para mostrar las imagenes en la galeria de usuarios
@app.route('/usu/galeria')
def usu_galeria():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY created_at DESC")
    imagenes = cursor.fetchall()
    conexion.commit()
    print(imagenes)
    return render_template('usu/galeria_usu.html', imagenes=imagenes) 

# Home de usuarios
@app.route('/home_usu')
def home_usu():
    return render_template('usu/home_usu.html')

# Ruta home de admin
@app.route('/home_admin')
def home_admin():
    return render_template('admin/home_admin.html')
  
  
if __name__ == '__main__':
  app.run(debug=True)  
  