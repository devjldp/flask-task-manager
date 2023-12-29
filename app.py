import os
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

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Define una ruta principal "/" que devuelve "Hello world... again!"


@app.route("/")
@app.route("/get_tasks")
def get_tasks():
    tasks = mongo.db.tasks.find()
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html"
                           )


# Si se ejecuta este archivo como script principal
if __name__ == "__main__":
    # Ejecuta la aplicación Flask con la configuración proporcionada por las variables de entorno
    app.run(
        host=os.environ.get("IP"),  # Obtiene el IP de las variables de entorno
        # Obtiene el puerto de las variables de entorno
        port=int(os.environ.get("PORT")),
        debug=True  # Activa el modo de depuración
    )
