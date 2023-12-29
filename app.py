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
    tasks = list(mongo.db.tasks.find())
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
        return redirect(url_for("profile", username=session["user"]))

    # Renderiza el template para el registro de usuarios
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # comprobar is existe el usuario
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash(f"Welcome, {request.form.get('username')}")
                return redirect(url_for("profile", username=session["user"]))
            else:
                # paswword incorrecto
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        else:
            # User no existe
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
    return render_template("login.html")


@app.route("/profile/<username>")
def profile(username):
    # grab the session user's matches
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for('login'))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        task = {
            "category_name": request.form.get("category_name"),
            "task_name": request.form.get("task_name"),
            "task_description": request.form.get("task_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        mongo.db.tasks.insert_one(task)
        flash("Task Successfully Added")
        return redirect(url_for("get_tasks"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_task.html", categories=categories)


# Si se ejecuta este archivo como script principal
if __name__ == "__main__":
    # Ejecuta la aplicación Flask con la configuración de las variables de entorno
    app.run(
        host=os.environ.get("IP"),  # Obtiene el IP de las variables de entorno
        # Obtiene el puerto de las variables de entorno
        port=int(os.environ.get("PORT")),
        debug=True  # Activa el modo de depuración
    )
