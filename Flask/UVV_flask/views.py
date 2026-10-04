def init_app(app):
    """
    Factory Secundario
    """
    @app.route('/')
    def index():
        return 'Ola mundo! lalalala'

    @app.route('/contato')
    def contato():
        return "<form><input type='text'></form>"