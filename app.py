from flask import Flask, jsonify, request, render_template, send_file, url_for, redirect, session
from psycopg2 import connect, extras
from passlib.hash import bcrypt
from flask_bootstrap import Bootstrap
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
import os

UPLOAD_FOLDER = 'static/img/'
ALLOWED_EXTENSIONS = {'txt','pdf','png','jpg','jpeg','gif'}

app = Flask(__name__)
csrf = CSRFProtect(app)
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

# Home de inicio de sitio
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

# Ruta home de admin
@app.route('/home_admin')
def home_admin():
    return render_template('admin/home_admin.html')
  
# Ruta para registrar los productos
@app.route('/admin')
def admin():
    email = session['email']
    admin = session['admin']
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM productos WHERE email=%s AND administrador=%s', [email,admin])
    productos = cursor.fetchall()
    conexion.commit()
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for record in productos:
        insertObject.append(dict(zip(columnName, record)))
    cursor.close()
    conexion.close() 
    return render_template('admin/admin.html', productos=insertObject)

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

# Borrar los datos de la tabla y las imagenes del img de static
@app.route('/admin/borrar', methods=['POST'])
def admin_borrar():
    _id = request.form['id']
    if not _id:
        return redirect(url_for('admin'))
    print(_id)
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM productos WHERE id_productos=%s",(_id,))
    producto = cursor.fetchone()
    conexion.commit()
    print(producto)
    if producto:
        imagen_path = os.path.join(UPLOAD_FOLDER, producto[0])
        if os.path.exists(imagen_path):
            os.unlink(imagen_path)
        cursor.execute("DELETE FROM productos WHERE id_productos=%s", (_id,))
        conexion.commit()   
    return redirect(url_for('admin'))

# Ruta para los posts del administrador 
@app.route('/admin_posts/')
def admin_posts():
    admin = session['admin']
    email = session['email']
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM posts_admin WHERE email=%s AND administrador=%s ORDER BY created_at DESC",[email,admin])
    posts = cursor.fetchall()
    conexion.commit()
    insertObject = []
    columnName = [column[0] for column in cursor.description]
    for record in posts:
        insertObject.append(dict(zip(columnName, record)))
    cursor.close()    
    return render_template('admin/posts_admin.html', posts=insertObject)

# Ruta para los posts que crea el administrador
@app.route('/crear_post_admin/', methods=['GET','POST'])
def crear_post_admin():
    admin = session['admin']
    email = session['email']
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO posts_admin(email,administrador,titulo,contenido) VALUES (%s,%s,%s,%s)",(email, admin, titulo, contenido))
    conexion.commit()
    return redirect(url_for('admin_posts'))

# Ruta para editar post del administrador
@app.route('/editar_post/<int:id>', methods=['POST'])
def editar_post(id):
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    fecha = request.form['fecha']
    if titulo and contenido and fecha:
        conexion = get_connection()
        cursor = conexion.cursor()
        sql = ("UPDATE posts_admin SET titulo=%s, contenido=%s, created_at=%s WHERE id_posts=%s")
        data = (titulo, contenido, fecha, id,)
        cursor.execute(sql,data)
        conexion.commit() 
    return redirect(url_for('admin_posts'))

# Ruta para eliminar post del administrador
@app.route('/eliminar_post/<string:id>')
def eliminar_post(id):
    conexion = get_connection()
    cursor = conexion.cursor()
    sql = ("DELETE FROM posts_admin WHERE id_posts=%s")
    data = (id,)
    cursor.execute(sql,data)
    conexion.commit()
    return redirect(url_for('admin_posts'))

# Ruta de los posts en usuarios
@app.route('/posts_usu/')
def posts_usu():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM posts_admin ORDER BY created_at DESC")
    posts = cursor.fetchall()
    conexion.commit()
    return render_template('usu/posts_usu.html', posts=posts)

"""# Ruta de los comentarios de los posts
@app.route('/messages', methods=['GET'])
def get_messages():
    usuario = session['usuario']
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM comentarios_usu WHERE usuario=%s ORDER BY created_at ASC ", [usuario])
    rows = cursor.fetchall()
    messages = []
    for row in rows:
        message = {
            'id_coment': row[0],
            'mensaje': row[1],
            'usuario': row[2],
            'created_at': row[3]
        }
        messages.append(message)
    cursor.close()
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def add_messages():
    usuario = session['usuario']
    mensaje = request.form['mensaje']
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO comentarios_usu (mensaje,usuario) VALUES (%s,%s)", (mensaje, usuario))
    cursor.close()
    conexion.commit()
    return render_template('usu/comentarios_usu.html')"""

@app.route('/comentarios_usu/')
def comentarios_usu():
    return render_template('usu/comentarios_usu.html')

# Home de usuarios
@app.route('/home_usu/')
def home_usu():
    conexion = get_connection()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos ORDER BY created_at DESC LIMIT 6")
    imagenes = cursor.fetchall()
    cursor.execute("SELECT * FROM posts_admin ORDER BY created_at DESC LIMIT 3")
    posts2 = cursor.fetchall()   
    return render_template('usu/home_usu.html', imagenes=imagenes, posts2=posts2)
    
# Cerrar sesión
@app.route('/logout')
def logout():
    message = ''
    session.pop['loggedin',None]
    session.pop['id',None]
    session.pop['email',None]
    message = 'Sesión cerrada con exito!!!'
    return render_template('sitio/home.html')


  
  
if __name__ == '__main__':
  app.run(debug=True)  
  