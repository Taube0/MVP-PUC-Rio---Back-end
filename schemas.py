from pydantic import BaseModel
from typing import Optional, List

# Base de inputs
class FilmeSchema(BaseModel):
    titulo: str
    ano: int
    genero: str
    descricao: Optional[str]

# Base para adicionar um filme
class FilmeViewSchema(FilmeSchema):
    id: int

# Base para visualizar a lista de filmes
class FilmeListSchema(BaseModel):
    filmes: List[FilmeViewSchema]

# Base para erros
class ErrorSchema(BaseModel):
    message: str

# Base para busca do ID de um filme
class FilmeBuscaSchema(BaseModel):
    id: int = 1  
