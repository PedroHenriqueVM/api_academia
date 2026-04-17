# 🏋️ API Academia

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-API-black)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange)
![JWT](https://img.shields.io/badge/Auth-JWT-green)
![Status](https://img.shields.io/badge/status-concluído-brightgreen)

API REST desenvolvida em **Python com Flask** para gerenciamento de alunos de academia e controle de acesso por catraca.

O sistema permite:

* cadastro de alunos
* controle de mensalidade
* verificação de acesso na catraca
* autenticação com JWT
* persistência de dados no Firebase Firestore
* documentação automática via Swagger

---

# 🚀 Deploy da API

🔗 **API online na Vercel**

https://api-academia-xi.vercel.app/

---

# 💻 Repositório do Projeto

🔗 GitHub

https://github.com/PedroHenriqueVM/api_academia.git

---

# 📖 Documentação da API

Swagger UI disponível em:

```text
https://api-academia-xi.vercel.app/apidocs
```

---

# 📚 Funcionalidades

✔ Login de administrador
✔ Cadastro de alunos
✔ Listagem de alunos
✔ Buscar aluno por ID
✔ Atualizar aluno
✔ Deletar aluno
✔ Verificação de acesso na catraca
✔ Integração com Firebase Firestore
✔ Autenticação JWT
✔ Documentação Swagger

---

# 🛠 Tecnologias utilizadas

* Python
* Flask
* Firebase Firestore
* JWT
* Flask-CORS
* Python Dotenv
* Flasgger (Swagger)
* Vercel

---

# 📂 Estrutura do Projeto

```
api_academia
│
├── app.py
├── auth.py
├── openapi.yaml
├── firebase.json
├── .env
├── requirements.txt
└── README.md
```

---

# ⚙️ Instalação do Projeto

## 1️⃣ Clonar repositório

```
git clone https://github.com/PedroHenriqueVM/api_academia.git
```

```
cd api_academia
```

---

## 2️⃣ Criar ambiente virtual

```
python -m venv venv
```

Ativar ambiente virtual

Windows

```
venv\Scripts\activate
```

Linux / Mac

```
source venv/bin/activate
```

---

## 3️⃣ Instalar dependências

```
pip install -r requirements.txt
```

---

# 🔑 Configuração do .env

Crie um arquivo `.env` na raiz do projeto.

```
SECRET_KEY=senha123
ADM_USUARIO=admin
ADM_SENHA=adm
```

---

# 🔥 Configuração do Firebase

1. Criar projeto no Firebase
2. Ativar **Firestore Database**
3. Criar credenciais de **Service Account**
4. Baixar o arquivo JSON
5. Renomear para:

```
firebase.json
```

Colocar na raiz do projeto.

---

# ▶️ Executar a API

```
python app.py
```

Servidor rodará em:

```
http://localhost:5000
```

---

# 🔐 Autenticação

Algumas rotas exigem **token JWT**.

## Login

```
POST /login
```

Body

```json
{
 "usuario": "admin",
 "senha": "adm"
}
```

Resposta

```json
{
 "message": "Login realizado com sucesso!",
 "token": "SEU_TOKEN"
}
```

Utilizar token nas rotas protegidas:

```
Authorization: Bearer SEU_TOKEN
```

---

# 📡 Rotas principais

## Listar alunos

```
GET /alunos
```

---

## Buscar aluno por ID

```
GET /alunos/{id}
```

---

## Criar aluno

```
POST /alunos
```

Body

```json
{
 "nome": "João Silva",
 "cpf": "12345678900",
 "status": "ATIVO"
}
```

---

## Atualizar aluno

```
PUT /alunos/{id}
```

---

## Deletar aluno

```
DELETE /alunos/{id}
```

---

## Controle da catraca

```
POST /catraca
```

Body

```json
{
 "cpf": "12345678900"
}
```

Resposta possível

```json
{
 "status": "LIBERADO"
}
```

ou

```json
{
 "status": "BLOQUEADO"
}
```

---

# 🧪 Testes da API

A API pode ser testada utilizando:

* Thunder Client
* Postman
* Swagger UI

---

# 📊 Banco de dados

Os dados são armazenados no **Firebase Firestore**.

Coleção principal:

```
alunos_academia
```

Exemplo de documento:

```
id: 1
nome: João Silva
cpf: 12345678900
status: ATIVO
```

---

# 👨‍💻 Autor

Pedro Henrique

Projeto desenvolvido para fins educacionais no curso de **Desenvolvimento de Sistemas**.
