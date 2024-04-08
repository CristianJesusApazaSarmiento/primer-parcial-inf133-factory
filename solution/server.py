from http.server import HTTPServer, BaseHTTPRequestHandler
import json 
from urllib.parse import urlparse, parse_qs

ordenes = []
contadorID = len(ordenes)

class Orden:
    def __init__(self, orden_type, id, client, status, payment, shipping, products, code, expiration):
        self.orden_type = orden_type
        self.id = id
        self.client = client
        self.status = status
        self.payment = payment
        self.shipping = shipping
        self.products = []
        self.code = code
        self.expiration = expiration
        
class OrdenCompra:
    def __init__(self, orden_type, id, client, status, payment, shipping, products, code, expiration):
        self.orden_type = orden_type
        self.id = id
        self.client = client
        self.status = status
        self.payment = payment
        self.shipping = shipping
        for producto in enumerate(products):
            self.products = producto
        self.code = code
        self.expiration = expiration

class Fisica(OrdenCompra):
    def __init__(self, id, client, status, payment, shipping, products, code, expiration):
        super().__init__("fisico", id, client, status, payment, shipping, products, code, expiration)

class Digital(OrdenCompra):
    def __init__(self, id, client, status, payment, shipping, products, code, expiration):
        super().__init__("digital", id, client, status, payment, shipping, products, code, expiration)


class OrdenFactory:
    @staticmethod
    def create_orden(orden_type, id, client, status, payment, shipping, products, code, expiration):
        if orden_type == "fisico":
            return Fisica(id, client, status, payment, shipping, products, code, expiration)
        elif orden_type == "digital":
            return Digital(id, client, status, payment, shipping, products, code, expiration)
        else:
            raise ValueError("Tipo de orden no válido")

class OrdenService:
    def __init__(self):
        self.factory = OrdenFactory()

    def agregar_orden(self, data):
        global contadorID
        contadorID += 1
        orden_type = data.get("orden_type", None)
        id = data.get("id", None)
        client = data.get("client", None)
        status = data.get("status", None)
        payment = data.get("payment", None)
        shipping = data.get("shipping", None)
        products = data.get("products", [])
        code = data.get("code", None)
        expiration = data.get("expiration", None)

        orden = self.factory.create_orden(orden_type, contadorID, client, status, payment, shipping, products, code, expiration)
        ordenes.append(orden.__dict__)
        return {
            'orden_type': orden.orden_type, 'id':orden.id, 'client': orden.status, 'payment': orden.payment, 'shipping': orden.payment, 'shipping': orden.shipping, 'products': orden.products, 'code': orden.code, 'expiration':orden.expiration
        }

    def actualizar_orden(self, id, data):
        index = self.buscar_index_por_id(id)
        if index!=None:
            orden = ordenes[index]
            client = data.get("client", None)
            status = data.get("status", None)
            payment = data.get("payment", None)
            shipping = data.get("shipping", None)
            products = data.get("products", [])
            code = data.get("code", None)
            expiration = data.get("expiration", None)
            orden.update ({
                "client":client, "status": status, "payment": payment, "shipping": shipping, "products": products, "code": code, "expiration": expiration
            })
            return orden
        else:
            return None

    def eliminar_orden(self, id):
        index = self.buscar_index_por_id(id)
        if index!=None:
            for orden in ordenes:
                if orden["id"]==id:
                    return ordenes.pop(index)
        else:
            return None

    def buscar_index_por_id(self, id):
        return next(
            (ordenes.index(orden) for orden in ordenes if orden["id"]==id), None,
        )
        
    def buscar_pedidos(self, data):
        listPedidos=[]
        for orden in ordenes:
            if orden["status"]==data:
                listPedidos.append(orden)
        return listPedidos
        
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        data = handler.rfile.read(content_length)
        return json.loads(data.decode("utf-8"))

class OrdenRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.orden_service = OrdenService()
        super().__init__(*args, **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        query_params = parse_qs(parsed.query)
        if self.path == "/orders":
            HTTPDataHandler.handle_response(self, 200, ordenes)
        elif parsed.path == "/orders":
            if "status" in query_params:
                status= query_params["status"][0]
                ordenes_obtenidos = self.orden_service.buscar_pedidos(status)
                if ordenes_obtenidos !=[]:
                    HTTPDataHandler.handle_response(self, 200, ordenes_obtenidos)
                else:
                    HTTPDataHandler.handle_response(self, 204, [])
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})
            
    def do_POST(self):
        if self.path == "/orders":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.orden_service.agregar_orden(data)
            HTTPDataHandler.handle_response(self, 201, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

    def do_PUT(self):
        if self.path.startswith("/orders/"):
            id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.orden_service.actualizar_orden(id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 404, {"Mensaje": "Orden no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Mensaje": "Ruta no encontrada"})

    def do_DELETE(self):
        if self.path.startswith("/orders/"):
            id = int(self.path.split("/")[-1])
            response_data = self.orden_service.eliminar_orden(id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, {"Mensaje": "Orden eliminada"})
            else:
                HTTPDataHandler.handle_response(self, 404, {"Mensaje": "Orden no encontrado"})
        else:
            HTTPDataHandler.handle_response(self, 404, {"Mensaje": "Ruta no encontrada"})


def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, OrdenRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()

if __name__ == "__main__":
    main()    