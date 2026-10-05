# Fase de configuracao
    # 1. declaracao de criacao do app
    app = Flask(__name__)

    # 2. especificacao da configuracao
    app.config

    # 3. registro de rotas
    @app.route('/')

    # 4. registro de blueprint
    app.register_blueprint(main)

    # 5. carregamento de modulos
    app.init_app(app)

    # 6. registro de hooks
    @app.before_request
    def before():
        pass

    @app.errorhandler(404)
    def not_found(error)
        return "Nao encontrado", 404

# Contexto de aplicacao
    1. acessar a variavel app
    2. acessar alguma variavel declarada com g (global)
    3. acessar o current_app

# Contexto de requisicao (esse contexto começa apenas após a primeira requisicao feita)
    1. cabecalhos HTTP
    2. parametros URLs
    3. dados de formularios
    4. objeto request
