from fastapi import FastAPI, Depends
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models.tipo import Tipo
from models.usuario import Usuario,LoginRequest, UsuarioUpdate
from models.biorreactor import Biorreactor,BiorreactorUpdate
from models.sensores import Sensor
from models.empresas import Empresa
from models.registro import Registro
from models.lectura_sensores import LecturaSensores

from services.tipo_service import TipoService, get_tipo_service
from services.usuario_service import UsuarioService, get_usuario_service
from services.biorreactor_service import  BiorreactorService, get_biorreactor_service
from services.sensores_service import SensorService, get_sensor_service
from services.empresas_service import EmpresaService, get_empresa_service
from services.registro_service import RegistroService, get_registro_service
from services.lectura_sensores_service import LecturaService, get_lectura_service




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

@app.get("/")
def read_root():
    return {"message": "Backend OK"}


# Tipo API routes

@app.post("/tipo/", response_model=Tipo)
async def create_tipo(tipo: Tipo, service: TipoService = Depends(get_tipo_service)):
    service.create_tipo(tipo)
    return tipo

@app.get("/tipo/{idTipo}", response_model=Tipo)
async def get_tipo(idTipo: int, service: TipoService = Depends(get_tipo_service)):
    return service.get_tipo(idTipo)

@app.get("/tipo/", response_model=List[Tipo])
async def get_all_tipo(service: TipoService = Depends(get_tipo_service)):
    return service.get_all_tipo()

@app.put("/tipo/{idTipo}", response_model=Tipo)
async def update_tipo(idTipo: int, tipo: Tipo, service: TipoService = Depends(get_tipo_service)):
    return service.update_tipo(idTipo, tipo)

@app.delete("/tipo/{idTipo}")
async def delete_tipo(idTipo: int, service: TipoService = Depends(get_tipo_service)):
    service.delete_tipo(idTipo)
    return {"message": "Tipo eliminado correctamente"}


# Usuario API routes


@app.post("/usuario/", response_model=Usuario)
async def create_usuario(usuario: UsuarioUpdate, service: UsuarioService = Depends(get_usuario_service)):
    try:
        return service.create_usuario(usuario)
    except Exception as e:
        print("❌ Error al crear usuario:", e)
        raise HTTPException(status_code=500, detail="Error al crear usuario")

@app.post("/usuario/login", response_model=Usuario)
async def login_usuario(data: LoginRequest, service: UsuarioService = Depends(get_usuario_service)):
    print(f"Login recibido: {data.email} - {data.password}")
    return service.login(data.email, data.password)

@app.get("/usuario/{idUsuario}", response_model=Usuario)
async def get_usuario(idUsuario: int, service: UsuarioService = Depends(get_usuario_service)):
    return service.get_usuario(idUsuario)

@app.get("/usuario/", response_model=List[Usuario])
async def get_all_usuarios(service: UsuarioService = Depends(get_usuario_service)):
    return service.get_all_usuarios()

@app.put("/usuario/{idUsuario}", response_model=Usuario)
async def update_usuario(idUsuario: int, usuario: Usuario, service: UsuarioService = Depends(get_usuario_service)):
    return service.update_usuario(idUsuario, usuario)

@app.delete("/usuario/{idUsuario}")
async def delete_usuario(idUsuario: int, service: UsuarioService = Depends(get_usuario_service)):
    service.delete_usuario(idUsuario)
    return {"message": "Usuario eliminado correctamente"}






# Biorrecator API routes

# Crear un biorreactor
@app.post("/biorreactor/", response_model=Biorreactor)
async def create_biorreactor(
    bior: BiorreactorUpdate,
    service: BiorreactorService = Depends(get_biorreactor_service)
):
    try:
        return service.create_biorreactor(bior)
    except Exception as e:
        print("❌ Error al crear biorreactor:", e)
        raise HTTPException(status_code=500, detail="Error al crear biorreactor")

# Obtener biorreactor por ID
@app.get("/biorreactor/{idBiorreactor}", response_model=Biorreactor)
async def get_biorreactor(
    idBiorreactor: int,
    service: BiorreactorService = Depends(get_biorreactor_service)
):
    return service.get_biorreactor(idBiorreactor)

# Obtener todos los biorreactores
@app.get("/biorreactor/", response_model=List[Biorreactor])
async def get_all_biorreactores(
    service: BiorreactorService = Depends(get_biorreactor_service)
):
    return service.get_all_biorreactores()

# Actualizar biorreactor
@app.put("/biorreactor/{idBiorreactor}", response_model=Biorreactor)
async def update_biorreactor(
    idBiorreactor: int,
    bior: Biorreactor,
    service: BiorreactorService = Depends(get_biorreactor_service)
):
    return service.update_biorreactor(idBiorreactor, bior)

# Eliminar biorreactor
@app.delete("/biorreactor/{idBiorreactor}")
async def delete_biorreactor(
    idBiorreactor: int,
    service: BiorreactorService = Depends(get_biorreactor_service)
):
    service.delete_biorreactor(idBiorreactor)
    return {"message": "Biorreactor eliminado correctamente"}



# Sensores API routes
@app.post("/sensores/", response_model=Sensor)
async def create_sensor(sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    sensor_id = service.create_sensor(sensor)
    return service.get_sensor(sensor_id)

@app.get("/sensores/{idSensores}", response_model=Sensor)
async def get_sensor(idSensores: int, service: SensorService = Depends(get_sensor_service)):
    return service.get_sensor(idSensores)

@app.get("/sensores/", response_model=List[Sensor])
async def get_all_sensores(service: SensorService = Depends(get_sensor_service)):
    return service.get_all_sensores()

@app.put("/sensores/{idSensores}", response_model=Sensor)
async def update_sensor(idSensores: int, sensor: Sensor, service: SensorService = Depends(get_sensor_service)):
    return service.update_sensor(idSensores, sensor)

@app.delete("/sensores/{idSensores}")
async def delete_sensor(idSensores: int, service: SensorService = Depends(get_sensor_service)):
    service.delete_sensor(idSensores)
    return {"message": "Sensor eliminado correctamente"}


# Empresa API routes
@app.post("/empresa/", response_model=Empresa)
async def create_empresa(empresa: Empresa, service: EmpresaService = Depends(get_empresa_service)):
    empresa_id = service.create_empresa(empresa)
    return service.get_empresa(empresa_id)

@app.get("/empresa/{idEmpresa}", response_model=Empresa)
async def get_empresa(idEmpresa: int, service: EmpresaService = Depends(get_empresa_service)):
    return service.get_empresa(idEmpresa)

@app.get("/empresa/", response_model=List[Empresa])
async def get_all_empresas(service: EmpresaService = Depends(get_empresa_service)):
    return service.get_all_empresas()

@app.put("/empresa/{idEmpresa}", response_model=Empresa)
async def update_empresa(idEmpresa: int, empresa: Empresa, service: EmpresaService = Depends(get_empresa_service)):
    return service.update_empresa(idEmpresa, empresa)

@app.delete("/empresa/{idEmpresa}")
async def delete_empresa(idEmpresa: int, service: EmpresaService = Depends(get_empresa_service)):
    service.delete_empresa(idEmpresa)
    return {"message": "Empresa eliminada correctamente"}

# registro API routes
@app.post("/registro/", response_model=Registro)
async def create_registro(registro: Registro, service: RegistroService = Depends(get_registro_service)):
    registro_id = service.create_registro(registro)
    return service.get_registro(registro_id)

@app.get("/registro/{idRegistro}", response_model=Registro)
async def get_registro(idRegistro: int, service: RegistroService = Depends(get_registro_service)):
    return service.get_registro(idRegistro)

@app.get("/registro/", response_model=List[Registro])
async def get_all_registros(service: RegistroService = Depends(get_registro_service)):
    return service.get_all_registros()

@app.put("/registro/{idRegistro}", response_model=Registro)
async def update_registro(idRegistro: int, registro: Registro, service: RegistroService = Depends(get_registro_service)):
    return service.update_registro(idRegistro, registro)

@app.delete("/registro/{idRegistro}")
async def delete_registro(idRegistro: int, service: RegistroService = Depends(get_registro_service)):
    service.delete_registro(idRegistro)
    return {"message": "Registro eliminado correctamente"}


# Lectura API routes

@app.post("/lectura/", response_model=LecturaSensores)
async def create_lectura(lectura: LecturaSensores, service: LecturaService = Depends(get_lectura_service)):
    lectura.estado_ambiente = calcular_estado_ambiente(lectura.temperatura, lectura.humedad)
    lectura_id = service.create_lectura(lectura)
    return service.get_lectura(lectura_id)

@app.get("/lectura/", response_model=List[LecturaSensores])
async def get_all_lecturas(service: LecturaService = Depends(get_lectura_service)):
    return service.get_all_lecturas()

@app.get("/lectura/{idLectura_sensores}", response_model=LecturaSensores)
async def get_lectura(idLectura_sensores: int, service: LecturaService = Depends(get_lectura_service)):
    return service.get_lectura(idLectura_sensores)

def calcular_estado_ambiente(temp: float, hum: float) -> str:
    if 26.8 <= temp <= 27.3 and 68 <= hum <= 80:
        return "Óptimo"
    elif temp < 25 or hum < 60 or hum > 80:
        return "Crítico"
    else:
        return "Ajustar"

@app.post("/lectura/", response_model=LecturaSensores)
async def create_lectura(lectura: LecturaSensores, service: LecturaService = Depends(get_lectura_service)):
    lectura.estado_ambiente = calcular_estado_ambiente(lectura.temperatura, lectura.humedad)
    lectura_id = service.create_lectura(lectura)
    return service.get_lectura(lectura_id)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)