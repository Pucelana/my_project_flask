""" Tabla de productos """
CREATE TABLE productos(
    id_productos SERIAL PRIMARY KEY NOT NULL,
    email VARCHAR(255) NOT NULL,
    administrador VARCHAR(255) NOT NULL,
    producto VARCHAR(255) NOT NULL,
    imagen TEXT NOT NULL,
    url VARCHAR(255) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    created_at DATE NOT NULL DEFAULT CURRENT_DATE
);
""" Tabla de los Administradores """
CREATE TABLE administradores(
    id_admin SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    primerApellido VARCHAR(50) NOT NULL,
    segundoApellido VARCHAR(50) NOT NULL,
    nombreUsuario VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    provincia VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""" Tabla de los Usuarios """
CREATE TABLE usuarios(
    id_usu SERIAL PRIMARY KEY NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    usuario VARCHAR(255) NOT NULL,
    correo VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
