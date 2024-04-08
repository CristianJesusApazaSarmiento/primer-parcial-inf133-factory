import requests

url = 'http://localhost:8000/'

new_order = {
    "orden_type": "fisica",
    "client": "Juan Perez",
    "status": "Pendiente",
    "payment": "Tarjeta de Crédito",
    "shipping": 10.0,
    "products": ["Camiseta", "Pantalón", "Zapatos"],
    "order_type": "Física"
}
response_crear = requests.post(url, json=new_order)
print(response_crear.json())

new_order = {
    "orden_type": "digital",
    "client": "Maria Rodriguez",
    "status": "Pendiente",
    "payment": "PayPal",
    "code": "ABC123",
    "expiration": "2022-12-31",
    "order_type": "Digital"
}
response_crear = requests.post(url, json=new_order)
print(response_crear.json())

response_listar = requests.get(url)
print(response_listar.json())

response_pendiente = requests.get(url + "?status=Pendiente")
print(response_pendiente.json())

orden_actualizada = {
    "status": "En Proceso"
}
response_actualizar = requests.put(url+ "orders/1", json=orden_actualizada)
print(response_actualizar.json())

response_eliminar = requests.delete(url + "orders/2")
print(response_eliminar.json())

new_order = {
    "orden_type": "fisica",
    "client": "Ana Gutierrez",
    "status": "Pendiente",
    "payment": "Tarjeta de Débito",
    "shipping": 20.0,
    "products": ["Licuadora", "Refrigeradora", "Lavadora"],
    "order_type": "Física"
}
response_crear = requests.post(url, json=new_order)
print(response_crear.json())