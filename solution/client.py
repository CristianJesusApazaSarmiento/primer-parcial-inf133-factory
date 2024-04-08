import requests

url = 'http://localhost:8000/orders'

new_order = {
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