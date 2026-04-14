from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from auth import token_obrigatorio, gerar_token
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv
from flasgger import Swagger
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.config['SWAGGER'] = {
    'openapi':'3.0.3'
} 
# Chama o OPENAPI para o código
swagger = Swagger(app, template_file='openapi.yaml')

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app, origins="*")

ADM_USUARIO = os.getenv("ADM_USUARIO")
ADM_SENHA = os.getenv("ADM_SENHA")

if os.getenv("VERCEL"):
    cred = credentials.Certificate(json.loads(os.getenv("FIREBASE_CREDENTIALS")))
else:
    cred = credentials.Certificate("firebase.json")

firebase_admin.initialize_app(cred)

db = firestore.client()


# ==========================
# ROTA PRINCIPAL
# ==========================

@app.route("/", methods=['GET'])
def root():
    return jsonify({
        "api":"academia",
        "version":"1.0",
        "Author":"Pedro"
    }), 200


# ==========================
# LOGIN
# ==========================

@app.route("/login", methods=['POST'])
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({"error":"Envie os dados para login"}), 400

    usuario = dados.get("usuario")
    senha = dados.get("senha")

    if not usuario or not senha:
        return jsonify({"error":"Usuário e senha são obrigatórios!"}), 400

    if usuario == ADM_USUARIO and senha == ADM_SENHA:
        token = gerar_token(usuario)
        return jsonify({
            "message":"Login realizado com sucesso!",
            "token":token
        }), 200

    return jsonify({"error":"Usuário ou senha inválidos"}), 401


# ==========================
# LISTAR ALUNOS
# ==========================

@app.route("/alunos", methods=['GET'])
def get_alunos():

    alunos = []
    lista = db.collection('alunos_academia').stream()

    for item in lista:
        alunos.append(item.to_dict())

    return jsonify(alunos), 200


# ==========================
# BUSCAR ALUNO POR ID
# ==========================

@app.route("/alunos/<int:id>", methods=['GET'])
def get_aluno_by_id(id):

    lista = db.collection('alunos_academia').where('id', '==', id).stream()

    for item in lista:
        return jsonify(item.to_dict()), 200

    return jsonify({"error":"Aluno não encontrado"}), 404


# ==========================
# CATRACA
# ==========================

@app.route("/catraca", methods=['POST'])
def catraca():

    dados = request.get_json()

    if not dados or "cpf" not in dados:
        return jsonify({"error":"CPF obrigatório"}), 400

    cpf = dados["cpf"]

    lista = db.collection("alunos_academia").where("cpf","==",cpf).stream()

    for item in lista:

        aluno = item.to_dict()

        if aluno["status"] == "ATIVO":
            return jsonify({
                "status":"LIBERADO"
            }), 200

        else:
            return jsonify({
                "status":"BLOQUEADO",
                "mensagem":"Procure a secretaria da academia"
            }), 403

    return jsonify({
        "status":"BLOQUEADO",
        "mensagem":"Aluno não encontrado"
    }), 404


# ===================================
# ROTAS PRIVADAS
# ===================================

# CRIAR ALUNO
@app.route("/alunos", methods=['POST'])
@token_obrigatorio
def post_aluno():

    dados = request.get_json()

    if not dados or "nome" not in dados or "cpf" not in dados:
        return jsonify({"error":"Dados inválidos!"}), 400

    try:

        contador_ref = db.collection("contador").document("controle_id")
        contador_doc = contador_ref.get()

        ultimo_id = contador_doc.to_dict().get("ultimo_id")

        novo_id = ultimo_id + 1

        contador_ref.update({"ultimo_id":novo_id})

        db.collection("alunos_academia").add({
            "id":novo_id,
            "nome":dados["nome"],
            "cpf":dados["cpf"],
            "status":dados.get("status","ATIVO")
        })

        return jsonify({"message":"Aluno cadastrado com sucesso!"}), 201

    except:
        return jsonify({"error":"Falha ao cadastrar aluno"}), 400

# ALTERAR ALUNO
@app.route("/alunos/<int:id>", methods=['PUT'])
@token_obrigatorio
def alunos_put(id):

    dados = request.get_json()

    if not dados or "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({"error":"Dados inválidos ou incompletos!"}), 400

    try:

        docs = db.collection("alunos_academia").where("id","==",id).limit(1).get()

        if not docs:
            return jsonify({"error":"Aluno não encontrado"}), 404

        for doc in docs:
            doc_ref = db.collection("alunos_academia").document(doc.id)
            doc_ref.update({
                "nome":dados["nome"],
                "cpf":dados["cpf"],
                "status":dados["status"]
            })

        return jsonify({"message":"Aluno atualizado com sucesso"}), 200

    except:
        return jsonify({"error":"Falha na atualização"}), 400

# DELETE ALUNO
@app.route("/alunos/<int:id>", methods=['DELETE'])
@token_obrigatorio
def delete_aluno(id):

    docs = db.collection("alunos_academia").where("id","==",id).limit(1).get()

    if not docs:
        return jsonify({"error":"Aluno não encontrado"}), 404

    doc_ref = db.collection("alunos_academia").document(docs[0].id)
    doc_ref.delete()

    return jsonify({"message":"Aluno excluído com sucesso"}), 200

# ERROS
@app.errorhandler(404)
def erro404(error):
    return jsonify({"error":"URL não encontrada"}), 404


@app.errorhandler(500)
def erro500(error):
    return jsonify({"error":"Servidor interno com falhas"}), 500


if __name__ == "__main__":
    app.run(debug=True)