from flask import Flask
from calculadora import calculadora_bp

app = Flask(__name__)

# Registra o Blueprint
app.register_blueprint(calculadora_bp, url_prefix = '/calc')

if __name__ == "__main__":
    app.run(debug=True)
