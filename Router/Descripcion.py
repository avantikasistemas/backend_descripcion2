from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from Class.Descripcion import Descripcion
from Utils.decorator import http_decorator
from Config.db import get_db

descripcion_router = APIRouter()

@descripcion_router.post('/descripcion/buscar', tags=["Descripcion"], response_model=dict)
@http_decorator
def buscar_por_numero(request: Request, db: Session = Depends(get_db)):
    """Busca documentos por número de pedido."""
    data = getattr(request.state, "json_data", {})
    numero = data.get("numero")
    response = Descripcion(db).buscar_por_numero(numero)
    return response

@descripcion_router.post('/descripcion/actualizar-descripciones', tags=["Descripcion"], response_model=dict)
@http_decorator
def actualizar_descripciones(request: Request, db: Session = Depends(get_db)):
    """Actualiza las descripciones de los documentos."""
    data = getattr(request.state, "json_data", {})
    response = Descripcion(db).actualizar_descripciones(data)
    return response
