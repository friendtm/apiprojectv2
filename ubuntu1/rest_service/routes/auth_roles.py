from flask import Blueprint, request, jsonify
from models.user_model import verify_password, add_user
from utils.jwt_utils import gerar_token
from utils.rabbitmq_utils import publicar_mensagem

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"erro": "Dados inválidos"}), 400

    if add_user(data["username"], data["password"]):
        publicar_mensagem("novo_utilizador", {"username": data["username"]})
        publicar_mensagem("novo_utilizador_ws", {"username": data["username"]})
        
        return jsonify({"mensagem": "Registo efetuado com sucesso."}), 201
    return jsonify({"erro": "Utilizador já existe."}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or "username" not in data or "password" not in data:
        return jsonify({"erro": "Dados inválidos"}), 400

    if verify_password(data["username"], data["password"]):
        token = gerar_token(data["username"])
        return jsonify({"token": token})
    return jsonify({"erro": "Credenciais inválidas."}), 401
