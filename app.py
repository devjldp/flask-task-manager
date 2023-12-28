import os
from flask import Flask

# Verifica si el archivo "env.py" existe y, de ser así, importa sus variables de entorno
if os.path.exists("env.py"):
    import env

# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define una ruta principal "/" que devuelve "Hello world... again!"


@app.route("/")
def hello():
    return "Hello world... again!"


# Si se ejecuta este archivo como script principal
if __name__ == "__main__":
    # Ejecuta la aplicación Flask con la configuración proporcionada por las variables de entorno
    app.run(
        host=os.environ.get("IP"),  # Obtiene el IP de las variables de entorno
        # Obtiene el puerto de las variables de entorno
        port=int(os.environ.get("PORT")),
        debug=True  # Activa el modo de depuración
    )
