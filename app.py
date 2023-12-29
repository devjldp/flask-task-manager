# Importa el módulo os para trabajar con funcionalidades del sistema operativo
import os
# Importa las clases y funciones necesarias de Flask y Flask-PyMongo
from flask import (Flask, flash, render_template,
                   redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# Verifica si el archivo "env.py" existe y, de ser así, importa sus variables de entorno
if os.path.exists("env.py"):
    import env

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos MongoDB y la clave secreta para la sesión
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

# Inicializa la conexión a la base de datos MongoDB usando Flask-PyMongo
mongo = PyMongo(app)

# Define una ruta principal "/" y "/get_tasks" para mostrar tareas desde la base de datos


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)

# Define la ruta "/register" para el registro de nuevos usuarios


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Comprueba si el nombre de usuario ya existe en la base de datos
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Registra al nuevo usuario en la base de datos
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # Inicia una sesión para el nuevo usuario
        session["user"] = request.form.get("username").lower()
        flash("Registration successful!")

    # Renderiza el template para el registro de usuarios
    return render_template("register.html")


# Si se ejecuta este archivo como script principal
if __name__ == "__main__":
    # Ejecuta la aplicación Flask con la configuración de las variables de entorno
    app.run(
        host=os.environ.get("IP"),  # Obtiene el IP de las variables de entorno
        # Obtiene el puerto de las variables de entorno
        port=int(os.environ.get("PORT")),
        debug=True  # Activa el modo de depuración
    )
