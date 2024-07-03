from flask import redirect, render_template
from flask_cors import CORS
import os
import logging
from db import init_db
from routes import register_routes
from dotenv import load_dotenv
from flask_openapi3 import OpenAPI, Info, Tag

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da documentação OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)

# Configuração do CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuração do banco de dados
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise RuntimeError("DATABASE_URL não está definido no .env")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Inicialize o banco de dados com a aplicação Flask
init_db(app)

# Definindo tags para a documentação
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
filme_tag = Tag(name="Filme", description="Adição, visualização e remoção de filmes na base de dados")

# Redirecionar para a documentação OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

# Servir a página HTML principal
@app.route('/index')
def index():
    return render_template('index.html')

# Registre as rotas definidas no routes.py
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
