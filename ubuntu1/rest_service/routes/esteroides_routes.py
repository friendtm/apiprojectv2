from flask import Blueprint, request, jsonify
from utils.jwt_utils import verificar_token
from jsonschema import validate, ValidationError
from database.mongo import collection
from utils.rabbitmq_utils import publicar_mensagem

esteroides_bp = Blueprint("esteroides", __name__)
esteroides = []

schema = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "preco": {"type": "number"},
        "categoria": {"type": "string"},
        "em_stock": {"type": "boolean"}
    },
    "required": ["nome", "preco", "categoria", "em_stock"]
}

def autenticar():
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return None
    return verificar_token(auth.split(" ")[1])

@esteroides_bp.route("/esteroides", methods=["GET"])
def listar():
    if not autenticar():
        return jsonify({"erro": "Token inválido ou ausente."}), 401
    
    resultados = list(collection.find({}, {"_id": 0}))  # Remove _id do Mongo para evitar erro de JSON
    return jsonify(resultados)

@esteroides_bp.route("/esteroides", methods=["POST"])
def adicionar():
    if not autenticar():
        return jsonify({"erro": "Token inválido ou ausente."}), 401
    try:
        dados = request.get_json()
        validate(instance=dados, schema=schema)
        
        dados_para_mensagem = dados.copy()
        collection.insert_one(dados)
        publicar_mensagem("nova_esteroide", {"tipo": "adicionado", **dados_para_mensagem})  # Fila Consumer.py
        publicar_mensagem("nova_esteroide_ws", {"tipo": "adicionado", **dados_para_mensagem})  # Fila Consumer_ws.py
        
        return jsonify({"mensagem": "Esteroide adicionado."})
    except ValidationError as e:
        return jsonify({"erro": str(e)}), 400
    
@esteroides_bp.route("/esteroides/<string:nome>", methods=["DELETE"])
def remover(nome):
    if not autenticar():
        return jsonify({"erro": "Token inválido ou ausente."}), 401

    resultado = collection.delete_one({"nome": nome})

    if resultado.deleted_count == 1:
        publicar_mensagem("remocao_esteroide", {"tipo": "removido", "nome": nome})
        publicar_mensagem("remocao_esteroide_ws", {"tipo": "removido", "nome": nome})
        
        return jsonify({"mensagem": f"Esteroide '{nome}' removido com sucesso."})
    else:
        return jsonify({"erro": f"Esteroide '{nome}' não encontrado."}), 404
