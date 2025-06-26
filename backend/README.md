py -m venv env

2
env\Scripts\activate

3
pip install -r requirements.txt

4. crear DB
python -c "from dao.db import init_db; init_db()"

5. ejecutar
py main.py

6
http://localhost:5000/usuarios

# Create product
curl -X POST "http://localhost:8000/products/" -H "Content-Type: application/json" -d '{"name":"Laptop","description":"Gaming laptop","price":999.99,"stock":10}'
curl -X POST "http://localhost:8000/products/" -H "Content-Type: application/json" -d '{"name":"Mouse","description":"Mouse Gaming","price":34,"stock":5}'

# Get product
curl "http://localhost:8000/products/1"

# Update product
curl -X PUT "http://localhost:8000/products/1" -H "Content-Type: application/json" -d '{"name":"Laptop","description":"Updated gaming laptop","price":1099.99,"stock":15}'

# Delete product
curl -X DELETE "http://localhost:8000/products/1"

# Create Client: POST /clients/
curl -X POST "http://localhost:8000/clients/" -H "Content-Type: application/json" -d '{"nombres":"Juan","apellidos":"Perez","correo":"juan.perez@example.com"}'

# Read Client: GET /clients/{client_id}
curl "http://localhost:8000/clients/1"

# Read All Clients: GET /clients/
curl "http://localhost:8000/clients/"

# Update Client: PUT /clients/{client_id}
curl -X PUT "http://localhost:8000/clients/1" -H "Content-Type: application/json" -d '{"nombres":"Juan","apellidos":"Perez","correo":"juan.perez2@example.com"}'

# Delete Client: DELETE /clients/{client_id}
curl -X DELETE "http://localhost:8000/clients/1"