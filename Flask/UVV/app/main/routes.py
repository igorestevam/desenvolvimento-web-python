from flask import current_app
from app.main import main

@main.route('/')
@main.route('/index')
def index():
    ambiente = current_app.config.get('ENV', 'desconhecido')
    return f'Ola, Mundo! Ambiente atual: {ambiente}.'