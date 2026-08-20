from flask import Blueprint, jsonify

calculadora_bp = Blueprint('calculadora', __name__)

@calculadora_bp.route('/soma/<int:a>/<int:b>')
def soma(a, b):
    resultado = a + b
    return jsonify({
        "operacao": "soma",
        "a": a,
        "b": b,
        "resultado": resultado
    })

@calculadora_bp.route('/subtracao/<int:a>/<int:b>')
def subtracao(a, b):
    resultado = a - b
    return jsonify({
        "operacao": "subtracao",
        "a": a,
        "b": b,
        "resultado": resultado
    })

@calculadora_bp.route('/divisao/<int:a>/<int:b>')
def divisao(a, b):
    resultado = a / b
    return jsonify({
        "operacao": "divisao",
        "a": a,
        "b": b,
        "resultado": resultado
    })

@calculadora_bp.route('/multiplicacao/<int:a>/<int:b>')
def multipicacao(a, b):
    resultado = a * b
    return jsonify({
        "operacao": "multipicacao",
        "a": a,
        "b": b,
        "resultado": resultado
    })
