instructions = [
        'DROP TABLE IF EXISTS ordenes;',
        'DROP TABLE IF  EXISTS usuario;',
        'DROP TABLE IF  EXISTS calendario;'


        """CREATE TABLE usuario (
            id  INT PRIMARY KEY AUTO_INCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        ); """,

        """CREATE TABLE ordenes (
            id  INT PRIMARY KEY AUTO_INCREMENT,
            folio INT NOT NULL,
            fecha DATE NOT NULL,
            estado TEXT NOT NULL,
            ciudad TEXT NOT NULL, 
            unidad TEXT NOT NULL,
            equipo TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            ns TEXT, niv TEXT, 
            servicio TEXT NOT NULL,
            ingeniero TEXT NOT NULL,
            contenido TEXT NOT NULL );""",  

        """CREATE TABLE calendario (
            id INT PRIMARY KEY AUTO_INCREMENT,
            titulo INT not NULL,
            fecha_i DATE NOT NULL,
            fecha_t DATE NOT NULL,
            URL VARCHAR NOT NULL);"""
]
