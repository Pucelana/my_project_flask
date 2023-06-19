""" Tabla de usuario """
CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
""" Tabla de productos """
CREATE TABLE productos(
    id_productos SERIAL PRIMARY KEY NOT NULL,
    producto VARCHAR(255) NOT NULL,
    imagen TEXT NOT NULL,
    url VARCHAR(255) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL
);
