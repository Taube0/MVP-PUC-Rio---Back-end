from flask_openapi3 import APIBlueprint, Tag
from models import Filme
from schemas import FilmeSchema, FilmeViewSchema, FilmeListSchema, ErrorSchema, FilmeBuscaSchema
from db import db

# Definindo as tags corretamente
filme_tag = Tag(name="Filme", description="Operações relacionadas a filmes")

# Define o index como página inicial da api
api = APIBlueprint('/', __name__)

# Rota para adicionar filmes com uso de schemas
@api.post('/adicionar', tags=[filme_tag],
          responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_filme(body: FilmeSchema):
    filme = Filme(
        titulo=body.titulo,
        ano=body.ano,
        genero=body.genero,
        descricao=body.descricao
    )

    try:
        db.session.add(filme)
        db.session.commit()
        return filme.to_dict(), 200
    except Exception as e:
        return {"message": str(e)}, 400

# Rota para listar todos os filmes
@api.get('/lista', tags=[filme_tag],
         responses={"200": FilmeListSchema, "404": ErrorSchema})
def get_filmes():
    filmes = Filme.query.all()
    if not filmes:
        return {"message": "Nenhum filme encontrado"}, 404
    return [filme.to_dict() for filme in filmes], 200

# Rota para buscar um filme específico através do ID
@api.get('/busca', tags=[filme_tag],
         responses={"200": FilmeBuscaSchema, "404": ErrorSchema})
def get_filme(query: FilmeBuscaSchema):
    filme_id = query.id
    filme = Filme.query.get(filme_id)
    if not filme:
        return {"message": "Filme não encontrado"}, 404
    return filme.to_dict(), 200

# Rota para excluir um dos filmes a partir do ID
@api.delete('/excluir', tags=[filme_tag],
            responses={"200": FilmeBuscaSchema, "404": ErrorSchema})
def delete_filme(query: FilmeBuscaSchema):
    filme_id = query.id
    filme = Filme.query.get(filme_id)
    if not filme:
        return {"message": "Filme não encontrado"}, 404
    try:
        db.session.delete(filme)
        db.session.commit()
        return {"message": "Filme removido com sucesso."}, 200
    except Exception as e:
        return {"message": str(e)}, 400

# Rota que atualiza os dados de um filme id
@api.put('/atualizar', tags=[filme_tag],
         responses={"200": FilmeBuscaSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_filme(query: FilmeBuscaSchema, body: FilmeSchema):
    filme_id = query.id
    filme = Filme.query.get(filme_id)
    if not filme:
        return {"message": "Filme não encontrado"}, 404

    try:
        filme.titulo = body.titulo
        filme.ano = body.ano
        filme.genero = body.genero
        filme.descricao = body.descricao

        db.session.commit()
        return filme.to_dict(), 200
    except Exception as e:
        return {"message": str(e)}, 400

def register_routes(app):
    app.register_api(api)
