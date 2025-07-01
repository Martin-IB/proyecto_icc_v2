from fastapi import FastAPI, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.biorreactor import Biorreactor
from models.usuario import Usuario
from models.lectura_sensores import LecturaSensor
from models.empresas import Empresa
from models.sensores import Sensor
from models.tipo import Tipo

from services.biorreactor_service import  BiorreactorService, get_biorreactor_service
from services.usuario_service import UsuarioService, get_usuario_service
from services.lectura_sensores_service import LecturaSensorService, get_lectura_sensor_service
from services.empresas_service import EmpresaService, get_empresa_service
from services.sensores_service import SensorService, get_sensor_service
from services.tipo_service import TipoService, get_tipo_service

from dao.db import init_db
from typing import List
import uvicorn
from typing import Optional
import time
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)
# Initialize database before starting the application
time.sleep(5)  # Espera adicional
init_db()  # inicializa la conexión una vez

@app.get("/")
def read_root():
    return {"message": "Backend OK"}

# Biorreactor API Routes
@app.post("/biorreactor/", response_model=Biorreactor)
async def create_biorreactor(biorreactor: Biorreactor, service:  BiorreactorService = Depends(get_biorreactor_service)):
    biorreactor_id = service.create_biorreactor(biorreactor)
    return await get_biorreactor(biorreactor_id, service)

@app.get("/biorreactor/{biorreactor_id}", response_model=Biorreactor)
async def get_biorreactor(biorreactor_id: int, service:  BiorreactorService = Depends(get_biorreactor_service)):
    return service.get_biorreactor(biorreactor_id)

@app.get("/biorreactor/", response_model=List[Biorreactor])
async def get_all_biorreactor(service:  BiorreactorService = Depends(get_biorreactor_service)):
    return service.get_all_biorreactor()

@app.put("/biorreactor/{biorreactor_id}", response_model=Biorreactor)
async def update_biorreactor(biorreactor_id: int, biorreactor: Biorreactor, service:  BiorreactorService = Depends(get_biorreactor_service)):
    return service.update_biorreactor(biorreactor_id, biorreactor)

@app.delete("/biorreactor/{biorreactor_id}")
async def delete_biorreactor(biorreactor_id: int, service:  BiorreactorService = Depends(get_biorreactor_service)):
    service.delete_biorreactor(biorreactor_id)
    return {"message": "Biorreactor deleted successfully"}




# Usuario API Routes
@app.post("/usuario/", response_model=Usuario)
async def create_usuario(usuario: Usuario, service: UsuarioService = Depends(get_usuario_service)):
    usuario_id = service.create_usuario(usuario)
    return await get_usuario(usuario_id, service)

@app.get("/usuario/{usuario_id}", response_model=Usuario)
async def get_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    return service.get_usuario(usuario_id)

@app.get("/usuario/", response_model=List[Usuario])
async def get_all_usuario(service: UsuarioService = Depends(get_usuario_service)):
    return service.get_all_usuario()

@app.put("/usuario/{usuario_id}", response_model=Usuario)
async def update_usuario(usuario_id: int, usuario: Usuario, service: UsuarioService = Depends(get_usuario_service)):
    return service.update_usuario(usuario_id, usuario)

@app.delete("/usuario/{usuario_id}")
async def delete_usuario(usuario_id: int, service: UsuarioService = Depends(get_usuario_service)):
    service.delete_usuario(usuario_id)
    return {"message": "Usuario deleted successfully"}


# Lectura API routes

@app.post("/lectura/", response_model=LecturaSensor)
async def create_lectura(lectura: LecturaSensor, service: LecturaSensorService = Depends(get_lectura_sensor_service)):
    lectura_id = service.create_lectura(lectura)
    return await get_lectura(lectura_id, service)

@app.get("/lectura/{lectura_id}", response_model=LecturaSensor)
async def get_lectura(lectura_id: int, service: LecturaSensorService = Depends(get_lectura_sensor_service)):
    return service.get_lectura(lectura_id)

@app.get("/lectura/", response_model=List[LecturaSensor])
async def get_all_lecturas(service: LecturaSensorService = Depends(get_lectura_sensor_service)):
    return service.get_all_lecturas()

@app.put("/lectura/{lectura_id}", response_model=LecturaSensor)
async def update_lectura(lectura_id: int, lectura: LecturaSensor, service: LecturaSensorService = Depends(get_lectura_sensor_service)):
    return service.update_lectura(lectura_id, lectura)

@app.delete("/lectura/{lectura_id}")
async def delete_lectura(lectura_id: int, service: LecturaSensorService = Depends(get_lectura_sensor_service)):
    service.delete_lectura(lectura_id)
    return {"message": "Lectura deleted successfully"}


# Empresas API routes

@app.post("/empresas/", response_model=Empresa)
async def create_empresa(empresa: Empresa, service: EmpresaService = Depends(get_empresa_service)):
    empresa_id = service.create_empresa(empresa)
    return service.get_empresa(empresa_id)

@app.get("/empresas/{empresa_id}", response_model=Empresa)
async def get_empresa(empresa_id: int, service: EmpresaService = Depends(get_empresa_service)):
    return service.get_empresa(empresa_id)

@app.get("/empresas/", response_model=List[Empresa])
async def get_all_empresas(service: EmpresaService = Depends(get_empresa_service)):
    return service.get_all_empresas()

@app.put("/empresas/{empresa_id}", response_model=Empresa)
async def update_empresa(empresa_id: int, empresa: Empresa, service: EmpresaService = Depends(get_empresa_service)):
    return service.update_empresa(empresa_id, empresa)

@app.delete("/empresas/{empresa_id}")
async def delete_empresa(empresa_id: int, service: EmpresaService = Depends(get_empresa_service)):
    service.delete_empresa(empresa_id)
    return {"message": "Empresa deleted successfully"}



# Sensores API routes

@app.post("/sensores/", response_model=Sensor)
async def create_sensor(sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    sensor_id = service.create_sensor(sensor)
    return service.get_sensor(sensor_id)

@app.get("/sensores/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    return service.get_sensor(sensor_id)

@app.get("/sensores/", response_model=List[Sensor])
async def get_all_sensores(service: SensorService = Depends(get_sensor_service)):
    return service.get_all_sensores()

@app.put("/sensores/{sensor_id}", response_model=Sensor)
async def update_sensor(sensor_id: int, sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    return service.update_sensor(sensor_id, sensor)

@app.delete("/sensores/{sensor_id}")
async def delete_sensor(sensor_id: int, service: SensorService = Depends(get_sensor_service)):
    service.delete_sensor(sensor_id)
    return {"message": "Sensor deleted successfully"}

# Tipo API routes

@app.post("/tipo/", response_model=Tipo)
async def create_tipo(tipo: Tipo, service: TipoService = Depends(get_tipo_service)):
    tipo_id = service.create_tipo(tipo)
    return service.get_tipo(tipo_id)

@app.get("/tipo/{tipo_id}", response_model=Tipo)
async def get_tipo(tipo_id: int, service: TipoService = Depends(get_tipo_service)):
    return service.get_tipo(tipo_id)

@app.get("/tipo/", response_model=List[Tipo])
async def get_all_tipo(service: TipoService = Depends(get_tipo_service)):
    return service.get_all_tipo()

@app.put("/tipo/{tipo_id}", response_model=Tipo)
async def update_tipo(tipo_id: int, tipo: Tipo, service: TipoService = Depends(get_tipo_service)):
    return service.update_tipo(tipo_id, tipo)

@app.delete("/tipo/{tipo_id}")
async def delete_tipo(tipo_id: int, service: TipoService = Depends(get_tipo_service)):
    service.delete_tipo(tipo_id)
    return {"message": "Tipo deleted successfully"}


@app.post("/login")
async def login(request: Request):
    data = await request.json()
    email = data.get("email")
    password = data.get("password")

    tipo_service = get_tipo_service()
    tipo = tipo_service.login(email, password)

    if tipo:
        return {
            "id": tipo.id,
            "nombre": tipo.nombre,
            "email": tipo.email,
            "tipo": "admin" if tipo.id == 1 else "usuario"
        }
    else:
        return JSONResponse(status_code=401, content={"detail": "Credenciales incorrectas"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)