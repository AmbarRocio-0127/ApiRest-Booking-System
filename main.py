"""Importación de librerías"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List

"""Creación de instancia FastAPI"""
app = FastAPI()

reservas: Dict[int, dict] = {}

# Esquemas (Modelos) Pydantic para representar los datos de un artículo.
class ReservaBase(BaseModel):
    """Esquema base con los campos comunes de una reserva."""
    huesped: str
    habitacion: int
    precio_noche: float
    notas: str | None = None
    
class ReservaCrear(ReservaBase):
    """Esquema de entrada utilizado para crear una reserva."""
    pass

class ReservaActualizar(BaseModel):
    """Esquema de entrada para actualizar parcialmente una reserva."""
    huesped: str | None = None
    habitacion: int | None = None
    precio_noche: float | None = None
    notas: str | None = None
    
class ReservaRespuesta(ReservaBase): 
    """Esquema de salida utilizado para devolver una reserva al cliente."""
    id: int
    
"""Endpoint raíz con mensaje inicial respecto al programa"""
@app.get("/")
def raiz():
    return JSONResponse(
        status_code=200,
        content={"exitos":True, "mensaje":"Sistema de reservas"}
    )

"""Endpoint de consulta (Read) que retorna todas las reservas."""
@app.get("/reservas/", response_model=List[ReservaRespuesta])
def obtener_reservas():
    if not reservas:
        return JSONResponse(
            status_code=404,
            content={"exito":False, "mensaje":"No se encontraron reservas disponibles"}
        )
    listado_reservas = [ReservaRespuesta(id=reserva_id, **datos).model_dump() for reserva_id, datos in reservas.
                        items()]
    
    return JSONResponse(
        status_code=200,
        content={"exito":True, "reserva": listado_reservas}
    )

"""Endpoint de consulta (Read) que retorna una reserva identificado mediante su ID.""" 
@app.get("/reservas/{reserva_id}/", response_model=ReservaRespuesta)
def obtener_reserva(reserva_id: int):
    if reserva_id not in reservas:
        return JSONResponse(
            status_code=404,
            content={"exito": False, "mensaje": "Reserva no disponible"}
        ) 
    
    return JSONResponse(
        status_code=200,
        content={"exito":True, "reserva": ReservaRespuesta(id=reserva_id, **reservas[reserva_id]).model_dump()}
    )
    
"""Endpoint de creación (Create). Recibe y valida los datos mediante el esquema ReservaCrear."""
@app.post("/reservas/", response_model=ReservaRespuesta)
def crear_reserva(reserva: ReservaCrear):
    reserva_id = len(reservas) + 1
    reservas[reserva_id] = reserva.model_dump()
    return JSONResponse(
        status_code=201,
        content={
            "exitos":True,
            "mensaje": "Reserva Registrada Correctamente",
            "reserva": ReservaRespuesta(id=reserva_id, **reservas[reserva_id]).model_dump()
        }
    )
    
"""Endpoint de actualización (Update) de una reserva existente."""
@app.put("/reservas/{reserva_id}/", response_model=ReservaRespuesta)
def actualizar_reserva(reserva_id: int, reserva: ReservaActualizar):
    if reserva_id not in reservas:
        return JSONResponse(
            status_code=404,
            content={"exito": False, "mensaje": "Reserva No Encontrada"}
        )
        
    reserva_guardada = reservas[reserva_id]
    reservas_actualizadas = reserva.model_dump(exclude_unset=True)
    reserva_guardada.update(reservas_actualizadas)
    reservas[reserva_id] = reserva_guardada
    
    return JSONResponse(
        status_code=200,
        content={
            "exito":True,
            "mensaje": "Reserva Actualizada Correctamente",
            "reserva": ReservaRespuesta(id=reserva_id, **reserva_guardada).model_dump()
        }
    )
    
"""Endpoint de eliminación (Delete) de una reserva existente."""
@app.delete("/reservas/{reserva_id}/", response_model=ReservaRespuesta)
def eliminar_reserva(reserva_id: int):
    if reserva_id not in reservas:
        return JSONResponse(
            status_code=404,
            content={"exito": False, "mensaje": "Reserva no registrada"}
        )
    
    reserva_eliminada = reservas.pop(reserva_id)
    
    return JSONResponse(
        status_code=200,
        content={
            "exito": True,
            "mensaje": f"Reserva {reserva_id} eliminada correctamente",
            "reserva": ReservaRespuesta(id=reserva_id, **reserva_eliminada).model_dump()
        }
    )