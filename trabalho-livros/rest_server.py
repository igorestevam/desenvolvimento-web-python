from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json

LIVROS = [
    {"id": 1,
     "titulo": "O Hobbit",
     "autor": "J.R.R. Tolkien",
     "ano": "1927",
     "disponivel": True,
    },
    {
        "id": 2,
        "titulo": "1984",
        "autor": "George Orwell",
        "ano": 1949,
        "disponivel": True,
    },
    {
        "id": 3,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899,
        "disponivel": False,
    },
    {
        "id": 4,
        "titulo": "O Pequeno Príncipe",
        "autor": "Antoine de Saint-Exupéry",
        "ano": 1943,
        "disponivel": True,
    },
    {
        "id": 5,
        "titulo": "Orgulho e Preconceito",
        "autor": "Jane Austen",
        "ano": 1813,
        "disponivel": True,
    },
    {
        "id": 6,
        "titulo": "A Revolução dos Bichos",
        "autor": "George Orwell",
        "ano": 1945,
        "disponivel": False,
    },
]

class RestHTTPRequestHandler(BaseHTTPRequestHandler):
    def send_json(self, status, data = None, headers = None):
        body = b""

        # se o conteúdo informado não for nulo, transforma o dicionário enviado e json
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
        # se o status não for "no content" envia mais um header retornando o tamanho do corpo da resposta
        if status != 204:
            self.send_header("Content-Length", str(len(body)))

        self.end_headers()

        # se o body existir, envia como corpo da resposta
        if body:
            self.wfile.write(body)

        # pega apenas o caminho do recurso do servidor (/api/livros)
        def _get_path(self):
            return urlsplit(self.path).path

        def do_GET(self):
            path = self.get_path()

            # se o caminho for "/api/livros" retorna todos os livros disponíveis
            if path == "/api/livros":
                self._send_json(200, [livro for livro in LIVROS if livro.get("disponivel") is True])
                return

            # se o caminho começar com "/api/livros/" (significa que será seguido por algum id de livro)
            if(path.startswith("/api/livros/")):
                # pega a última parte da url, ou seja, o id
                id_livro_texto = path.split("/")[-1]

                # tenta passar o id que foi pego na url de string para int. Se der errado, retorna erro
                try:
                    id_livro = int(user_id_text)
                except ValueError:
                    self.send_json(
                        400,
                        {"Erro": "Id invalido"}
                    )
                    return
                
                livro = next(
                    (livro for livro in LIVROS if livro["id"] == id_livro)
                )re
