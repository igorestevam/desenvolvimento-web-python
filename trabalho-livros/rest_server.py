from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json

BOOKS = [
    {
        "id": 1,
        "title": "O Hobbit",
        "author": "J.R.R. Tolkien",
        "year": 1937,
        "available": True,
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "available": True,
    },
    {
        "id": 3,
        "title": "Dom Casmurro",
        "author": "Machado de Assis",
        "year": 1899,
        "available": False,
    },
    {
        "id": 4,
        "title": "O Pequeno Principe",
        "author": "Antoine de Saint-Exupery",
        "year": 1943,
        "available": True,
    },
    {
        "id": 5,
        "title": "Orgulho e Preconceito",
        "author": "Jane Austen",
        "year": 1813,
        "available": True,
    },
    {
        "id": 6,
        "title": "A Revolucao dos Bichos",
        "author": "George Orwell",
        "year": 1945,
        "available": False,
    },
]

REQUIRED_FIELDS = {"title", "author", "year", "available"}


class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, data=None, headers=None):
        body = b""

        # se o conteudo informado nao for nulo, transforma o dicionario enviado em json
        if data is not None:
            body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        # se os headers informados existirem, envia eles para o header na resposta
        if headers:
            for name, value in headers.items():
                self.send_header(name, value)

        # se o status nao for "no content" envia mais um header retornando o tamanho do corpo da resposta
        if status != 204:
            self.send_header("Content-Length", str(len(body)))

        self.end_headers()

        # se o body existir, envia como corpo da resposta
        if body:
            self.wfile.write(body)

    # pega apenas o caminho do recurso do servidor (/api/books)
    def _get_path(self):
        return urlsplit(self.path).path

    # le e decodifica o corpo da requisicao como JSON, tratando os erros comuns
    def _read_json_body(self):
        content_length = self.headers.get("Content-Length")

        if content_length is None:
            self._send_json(411, {"error": "Content-Length is required"})
            return None, False

        try:
            length = int(content_length)
            data = self.rfile.read(length)
            parsed = json.loads(data)
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"error": "Invalid JSON"})
            return None, False

        if not isinstance(parsed, dict):
            self._send_json(400, {"error": "Expected a JSON object"})
            return None, False

        return parsed, True

    # valida se os campos obrigatorios estao presentes e possuem o tipo correto
    def _validate_book_payload(self, payload):
        missing_fields = REQUIRED_FIELDS - set(payload.keys())
        if missing_fields:
            self._send_json(
                400,
                {"error": f"Missing required field(s): {sorted(missing_fields)}"}
            )
            return False

        if not isinstance(payload.get("title"), str) or not payload["title"].strip():
            self._send_json(400, {"error": "Field 'title' must be a non-empty string"})
            return False

        if not isinstance(payload.get("author"), str) or not payload["author"].strip():
            self._send_json(400, {"error": "Field 'author' must be a non-empty string"})
            return False

        # bool e subtipo de int em Python, por isso e preciso verificar se e booleano tambem
        if not isinstance(payload.get("year"), int) or isinstance(payload.get("year"), bool):
            self._send_json(400, {"error": "Field 'year' must be an integer"})
            return False

        if not isinstance(payload.get("available"), bool):
            self._send_json(400, {"error": "Field 'available' must be a boolean"})
            return False

        return True

    def do_GET(self):
        path = self._get_path()

        # se o caminho for "/api/books", retorna todos os livros
        if path == "/api/books":
            self._send_json(200, BOOKS)
            return

        # se o caminho comecar com "/api/books/" (significa que tera algum id de livro depois da barra)
        if path.startswith("/api/books/"):
            # pega a ultima parte da url, ou seja, o id
            id_text = path.split("/")[-1]

            # tenta transformar o id que foi pego na url de string para int. Se der errado, retorna id invalido
            try:
                book_id = int(id_text)
            except ValueError:
                self._send_json(400, {"error": "Invalid id"})
                return

            # procura o livro na lista que tenha o id informado
            book = next((book for book in BOOKS if book["id"] == book_id), None)

            # se nao achar nenhum, retorna "nao encontrado"
            if book is None:
                self._send_json(404, {"error": "Book not found"})
                return

            # envia status "Ok" e o livro no corpo do json
            self._send_json(200, book)
            return

        # se a rota nao estiver correta, retorna "nao encontrada"
        self._send_json(404, {"error": "Route not found"})

    def do_POST(self):
        path = self._get_path()

        if path != "/api/books":
            self._send_json(404, {"error": "Route not found"})
            return

        new_book, ok = self._read_json_body()
        if not ok:
            return

        if not self._validate_book_payload(new_book):
            return

        # cria um id novo autoincrementado
        new_id = max((book["id"] for book in BOOKS), default=0) + 1

        # associa o novo id ao novo livro e coloca ele na lista "BOOKS"
        new_book["id"] = new_id
        BOOKS.append(new_book)

        # envia o JSON com o status "criado", os dados do novo livro e a url em que ele se encontra
        self._send_json(201, new_book, headers={"Location": f"/api/books/{new_id}"})

    def do_PUT(self):
        path = self._get_path()

        if not path.startswith("/api/books/"):
            self._send_json(404, {"error": "Route not found"})
            return

        id_text = path.split("/")[-1]
        try:
            book_id = int(id_text)
        except ValueError:
            self._send_json(400, {"error": "Invalid id"})
            return

        book = next((book for book in BOOKS if book["id"] == book_id), None)
        if book is None:
            self._send_json(404, {"error": "Book not found"})
            return

        updated_data, ok = self._read_json_body()
        if not ok:
            return

        if not self._validate_book_payload(updated_data):
            return

        book["title"] = updated_data["title"]
        book["author"] = updated_data["author"]
        book["year"] = updated_data["year"]
        book["available"] = updated_data["available"]

        self._send_json(200, book)

    def do_DELETE(self):
        path = self._get_path()

        # se a url nao comecar com "/api/books/" retorna rota nao encontrada
        if not path.startswith("/api/books/"):
            self._send_json(404, {"error": "Route not found"})
            return

        # pega o id do livro na url
        id_text = path.split("/")[-1]

        # tenta transformar o id informado pela url para int. Se nao conseguir, retorna id invalido
        try:
            book_id = int(id_text)
        except ValueError:
            self._send_json(400, {"error": "Invalid id"})
            return

        # procura em BOOKS o livro com o id procurado, exclui ele da lista e retorna "no content"
        for index, book in enumerate(BOOKS):
            if book["id"] == book_id:
                BOOKS.pop(index)
                self._send_json(204)
                return

        self._send_json(404, {"error": "Book not found"})


def run(server_class=HTTPServer,
        handler_class=RestHTTPRequestHandler,
        port=3001):
    server_address = ("127.0.0.1", port)
    httpd = server_class(server_address, handler_class)

    print(f"Servidor HTTP disponivel em "
          f"http://127.0.0.1:{port}")

    httpd.serve_forever()


if __name__ == "__main__":
    run()