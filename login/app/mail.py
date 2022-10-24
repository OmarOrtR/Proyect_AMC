from asyncio import events
from cgi import print_form
from distutils import errors
from distutils.log import error
from importlib.metadata import requires
from multiprocessing.sharedctypes import Value
from pydoc import ErrorDuringImport
from turtle import title
from flask import (
    Flask,  Blueprint, render_template, request, flash, url_for, redirect
)
from app.db import get_db
bp = Blueprint('mail', __name__, url_prefix="/")

# Inicio de Sesion
# utilizamos los dos metodos de get y post que nos ayudan a enviar y recibir informacion a partir de nuestr
# codigo de html. Enseguida creamos la funcion principal de login donde recuperamos dos variables iniciadoras.
# el nombre de usuario y contraseña, para esto comparamos con la base de datos, en donde se encuentros los
# usuarios dados de alta. Si hay coincidencia en un 100% con alguno de los usuarios existentes, esto nos va a
# permitirnos redirigirnos a la pagina de index. Si alguno de los dos datos ingresados no coincide, nos surgira
# un messagebox con la leyenda de volver a intentar el ingreso de los datos.


@bp.route('/', methods=['GET', 'POST'])
def login():
    db, c = get_db()

    if request.method == 'POST':
        # variables recopiladas de login.html
        username = request.form.get('username')
        password = request.form.get('password')
        errors = []

        # if not username:
        #     # comentarios de mal llenado de las celdas
        #     errors.append('Colocar un Usuario')
        # elif not password:
        #     errors.append('Colocar contraseña')

        if len(errors) == 0:
            c.execute(
                "SELECT username from usuario WHERE username like %s ", (username, ))  # comparacion con base de datos

            username_login = c.fetchall()
            username_login = len(username_login)

            if username_login != 0:  # usuarios registrados
                c.execute(
                    "SELECT password from usuario WHERE username like %s ", (username, ))

                password_login = c.fetchall()
                password_login = password_login[0]['password']

                while password_login != password:                                      # revision de contraseña

                    flash('Usuario no valido')
                    return render_template('mails/login.html')

            else:                                                                      # usuarios no registrados
                return render_template('mails/login.html')

            return redirect('index')

    return render_template('mails/login.html')

# Muestreo de Registros
# El muestreo de registros, nos enfocamos en los inputs de filtrado de la informacion, se hacen las condiciones
# de la manera en la que se quieren muestrear nuestros datos pertenecientes a la base de datos. Captura de la
# misma manera con el metodo Get que parte de nuestro codigo de html.


@bp.route('/index', methods=['GET', 'POST'])
def index():
    db, c = get_db()

    engineer = request.args.get('engineer')
    eliminar = request.args.get('eliminar')
    ciudad = request.args.get('ciudad')
    servicio = request.args.get('servicio')
    errors = []

    engineer_ = bool(engineer)
    ciudad_ = bool(ciudad)
    servicio_ = bool(servicio)
    eliminar_ = bool(eliminar)

# SI O NADA SIN ELIMINAR
    if engineer_ is False and ciudad_ is False and servicio_ is False and eliminar_ is False:  # no es tru ningun y muestra todo
        c.execute("SELECT * FROM ordenes")

    # selecciona los tres filtros y no eliminar
    elif engineer_ is True and ciudad_ is True and servicio_ is True and eliminar_ is False:
        c.execute("SELECT * FROM ordenes WHERE ciudad like %s AND ingeniero like %s AND servicio like %s",
                  ('%' + ciudad + '%', '%' + engineer + '%', '%' + servicio + '%',))

# ELIMINAR REGISTROS
    elif engineer_ is False and ciudad_ is False and servicio_ is False and eliminar_ is True:  # Eliminar registro
        c.execute("DELETE FROM ordenes WHERE folio = %s ", (eliminar, ))
        db.commit()

# FILTROS INDIVIDUALES
    elif engineer_ is True and ciudad_ is False and servicio_ is False and eliminar_ is False:  # selecciona por ingeniero

        c.execute("SELECT * FROM ordenes WHERE ingeniero like %s",
                  ('%' + engineer + '%', ))

    elif engineer_ is False and ciudad_ is True and servicio_ is False and eliminar_ is False:  # selecciona por ciudad

        c.execute("SELECT * FROM ordenes WHERE ciudad like %s ",
                  ('%' + ciudad + '%', ))

    elif engineer_ is False and ciudad_ is False and servicio_ is True and eliminar_ is False:  # selecciona por servicio

        c.execute("SELECT * FROM ordenes WHERE servicio like %s ",
                  ('%' + servicio + '%', ))


# FILTRADO EN PARES

    elif engineer_ is True and ciudad_ is True and servicio_ is False and eliminar_ is False:  # selecciona por ingeniero y ciudad

        c.execute("SELECT * FROM ordenes WHERE ingeniero like %s AND ciudad like %s",
                  ('%' + engineer + '%', '%' + ciudad + '%', ))

    # selecciona por ingeniero y servicio
    elif engineer_ is True and ciudad_ is False and servicio_ is True and eliminar_ is False:

        c.execute("SELECT * FROM ordenes WHERE ingeniero like %s AND servicio like %s",
                  ('%' + engineer + '%', '%' + servicio + '%', ))

    elif engineer_ is False and ciudad_ is True and servicio_ is True and eliminar_ is False:  # selecciona ciudad y servicio
        c.execute("SELECT * FROM ordenes WHERE ciudad like %s AND servicio like %s",
                  ('%' + ciudad + '%', '%' + servicio + '%', ))

    else:
        c.execute("SELECT * FROM ordenes")
        errors.append('No se acepta esta opción')
        for error in errors:
            flash(error)

    mails = c.fetchall()
    return render_template('mails/index.html', mails=mails)

# Registro de Ordenes de Servicio
# Esta pestaña nos ayuda a la captura de los datos y registro en nuestra base de datos. Una vez completado un registro
# nos aparece un mensaje de registro realizado redireccionando a la misma pestaña para la simplificacion de ubicacion
# cuando es necesario la captura de multiples ordenes de servicio


@bp.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == 'POST':

        # VARIABLES DE FORMULARIO
        folio = request.form.get('folio')
        fecha = request.form.get('fecha')
        ingeniero = request.form.get('ingeniero')
        estado = request.form.get('estado')
        ciudad = request.form.get('ciudad')
        unidad = request.form.get('unidad')
        equipo = request.form.get('equipo')
        marca = request.form.get('marca')
        modelo = request.form.get('modelo')
        ns = request.form.get('ns')
        niv = request.form.get('niv')
        servicio = request.form.get('servicio')
        contenido = request.form.get('contenido')

        errors = []

        if len(errors) == 0:
            db, c = get_db()

            c.execute("""INSERT INTO ordenes(
                        folio,fecha,estado,ciudad,unidad,equipo,marca,
                        modelo,ns,niv,servicio,ingeniero,contenido)
                        VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)""", (folio, fecha, estado, ciudad, unidad, equipo, marca, modelo, ns, niv, servicio, ingeniero, contenido))
            db.commit()

            flash("Registro realizado con éxito")

    return render_template('mails/create.html')

# Registro de Nuevos Usuarios


@bp.route('/new', methods=['GET', 'POST'])
# se ocupan los datos obtenidos de la pestaña new, con el metodo get y se ingresan a la base de datos en su respectivas
# tablas y celdas, antes se rectifica y verifica la contraseña. Si esto no coincide el programa nos pedira volver a repetir
# os pasos
def new():
    db, c = get_db()

    if request.method == 'POST':
        folio = request.form.get('nombre_u')
        contrasena = request.form.get('contraseña_u')
        verificacion = request.form.get('contraseña_u2')
        errors = []

        if verificacion != contrasena:
            errors.append("Contraseñas no coinciden")

        if len(errors) == 0:

            if contrasena == verificacion:
                c.execute(""" INSERT INTO usuario (
                username,password) VALUES (%s,%s)""", (folio, contrasena))
                db.commit()
                return redirect(url_for('mail.index'))
        else:
            for error in errors:
                flash(error)

    return render_template('mails/new.html')



# Agregar Eventos

@bp.route('/add', methods=['GET', 'POST'])
def add():
    db, c = get_db()

    if request.method == "POST":
        titulo = request.form.get('title')
        fecha_i = request.form.get('start')
        fecha_t = request.form.get('end')
        URL = request.form.get('url')

        print(titulo,fecha_t,fecha_i,URL)


        if fecha_t == '':
            fecha_t = fecha_i

        c.execute("""INSERT INTO calendario(
                titulo,fecha_i,fecha_t,URL)
                VALUES (%s, %s, %s,%s)""", (titulo,fecha_i,fecha_t,URL))
        db.commit()
        return redirect(url_for('mail.add'))

    return render_template("mails/add.html")


# Calendario
@bp.route('/calendar', methods=['GET', 'POST'])
def calendar():
    db, c = get_db()

    c.execute("SELECT * FROM calendario")

    events= c.fetchall()
    print(events)   
    return render_template('mails/calendar.html', events=events)
