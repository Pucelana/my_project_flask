""" Tabla de productos """
CREATE TABLE productos(
    id_productos SERIAL PRIMARY KEY NOT NULL,
    producto VARCHAR(255) NOT NULL,
    imagen TEXT NOT NULL,
    url VARCHAR(255) NOT NULL,
    genero VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL
);