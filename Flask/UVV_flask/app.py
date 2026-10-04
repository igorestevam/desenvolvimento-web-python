from flask import Flask
import views

# Callable padrão de fábrica de aplicativos (application factory), permitindo criar e retornar uma instância configurada da aplicação web de forma dinâmica
# usado também para nao fazermos a gambiarra de chamar o view depois do 'app = Flask(__name__)'
def create_app():
    "Factory principal"
    app = Flask(__name__)

    views.init_app(app)

    return app