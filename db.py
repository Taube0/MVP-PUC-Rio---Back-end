from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        load_initial_data()

def load_initial_data():
    from models import Filme

    # Carga inicial de filmes
    filmes_iniciais = [
        {"titulo": "O Poderoso Chefão", "ano": 1972, "genero": "Crime, Drama", "descricao": "A saga da família Corleone."},
        {"titulo": "O Senhor dos Anéis: A Sociedade do Anel", "ano": 2001, "genero": "Aventura, Fantasia", "descricao": "Um hobbit e oito companheiros embarcam em uma jornada para destruir o Anel do Poder."},
        {"titulo": "Pulp Fiction: Tempo de Violência", "ano": 1994, "genero": "Crime, Drama", "descricao": "As vidas de dois assassinos se entrelaçam em uma série de eventos bizarros."}
    ]

    try:
        for filme_data in filmes_iniciais:
            if not Filme.query.filter_by(titulo=filme_data["titulo"], ano=filme_data["ano"]).first():
                filme = Filme(**filme_data)
                db.session.add(filme)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao carregar dados iniciais: {e}")
