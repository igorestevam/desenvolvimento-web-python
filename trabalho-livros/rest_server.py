from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit
import json

LIVROS = [
    {"id": 1,
     "titulo": "O Hobbit",
     "autor": "J.R.R. Tolkien",
     "ano": 1927,
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
    def _send_json(self, status, data = None, headers = None):
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
        path = self._get_path()

        # se o caminho for "/api/livros", retorna todos os livros
        if path == "/api/livros":
            self._send_json(200, LIVROS)
            return

        # se o caminho começar com "/api/livros/" (significa que terá algum id de livro depois da barra)
        if(path.startswith("/api/livros/")):
            # pega a última parte da url, ou seja, o id
            id_livro_texto = path.split("/")[-1]

            # tenta passar o id que foi pego na url de string para int. Se der errado, retorna id inválido
            try:
                id_livro = int(id_livro_texto)
            except ValueError:
                self._send_json(400, {"Erro": "Id invalido"})
                return

            # procura o livro no dicionário que tenha o id informado
            livro = next((livro for livro in LIVROS if livro["id"] == id_livro), None)

            # se não achar nenhum, retorna "Não encontrado"
            if livro is None:
                self._send_json(404, {"Erro": "Livro não encontrado"})
                return

            # envia status "Ok" e o livro no corpo do json
            self._send_json(200, livro)
            return

        # se a rota não estiver correta, retorna "não encontrada"
        self._send_json(404, {"Erro": "Rota não encontrada"})

    def do_POST(self):
        path = self._get_path()

        if path != "/api/livros":
            self._send_json(404, {"Erro": "Rota não encontrada"})
            return

        content_length = self.headers.get("Content-Length")

        # se a quanidade de caracteres for nula, retorna erro
        if content_length is None:
            self._send_json(411, {"Erro": "Necessita de Content-Length"})
            return

        # tenta transformar para int o tamanho do corpo pego no header e depois transformar de JSON para dicionário em python
        try:
            length = int(content_length)
            data = self.rfile.read(length)
            novo_livro = json.loads(data)
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"Erro": "JSON inválido"})
            return

        # verifica se o novo livro é um dicionário
        if not isinstance(novo_livro, dict):
            self._send_json(400, {"Erro": "Esperado um objeto JSON"})
            return
        # verifica se o campo ano do novo livro é um inteiro
        if not isinstance(novo_livro.get("ano"), int):
            self._send_json(400, {"Erro": "Campo 'ano' deve ser um número inteiro"})
            return
        # verifica se o campo disponivel do novo livro é um booleano
        if not isinstance(novo_livro.get("disponivel"), bool):
            self._send_json(400, {"Erro": "Campo 'disponivel' deve ser um booleano"})
            return

        # pega os campos obrigatórios que não estão em novo_livro
        campos_nao_presentes = {"titulo", "autor", "ano", "disponivel"} - set(novo_livro.keys())

        # verifica se existem campos não informados em novo_livro
        if campos_nao_presentes:
            self._send_json(400, {"Erro": f"Campo(s) obrigatório(s) ausente(s): {list(campos_nao_presentes)}"})
            return

        # cria um id novo autoincrementado
        novo_id = max((livro["id"] for livro in LIVROS), default=0) + 1

        # associa o novo id ao novo livro e coloca ele na lista de dicionarios "LIVRO"
        novo_livro["id"] = novo_id
        LIVROS.append(novo_livro)

        # envia o JSON com o status "criado", os dados do novo livro e a url em que ele se encontra
        self._send_json(201, novo_livro, headers={"Location": f"/api/livros/{novo_id}"})

    def do_PUT(self):
        path = self._get_path()

        if not path.startswith("/api/livros/"):
            self._send_json(404, {"Erro": "Rota não encontrada"})
            return

        id_texto = path.split("/")[-1]
        try:
            id_livro = int(id_texto)
        except ValueError:
            self._send_json(400, {"Erro": "Id inválido"})
            return

        livro = next((livro for livro in LIVROS if livro["id"] == id_livro), None)
        if livro is None:
            self._send_json(404, {"Erro": "Livro não encontrado"})
            return

        content_length = self.headers.get("Content-Length")
        if content_length is None:
            self._send_json(411, {"Erro": "Necessita de Content-Length"})
            return

        try:
            length = int(content_length)
            data = self.rfile.read(length)
            dados_atualizados = json.loads(data)
        except (ValueError, json.JSONDecodeError):
            self._send_json(400, {"Erro": "JSON inválido"})
            return

        if not isinstance(dados_atualizados, dict):
            self._send_json(400, {"Erro": "Esperado um objeto JSON"})
            return

        campos_faltantes = {"titulo", "autor", "ano", "disponivel"} - set(dados_atualizados.keys())
        if campos_faltantes:
            self._send_json(400, {"Erro": f"Campo(s) obrigatório(s) ausente(s): {list(campos_faltantes)}"})
            return

        livro["titulo"] = dados_atualizados["titulo"]
        livro["autor"] = dados_atualizados["autor"]
        livro["ano"] = dados_atualizados["ano"]
        livro["disponivel"] = dados_atualizados["disponivel"]

        self._send_json(200, livro)

    def do_DELETE(self):
        path = self._get_path()

        # se a url não começar com "/api/livros/" retorna rota não encontrada
        if not path.startswith("/api/livros/"):
            self._send_json(404, {"Erro": "Rota não encontrada"})
            return

        # pega o id do livro na url
        id_livro_texto = path.split("/")[-1]

        # tenta transformar o id informado pela url para int. Se não conseguir, retorna id inválido
        try:
            id_livro = int(id_livro_texto)
        except ValueError:
            self._send_json(400, {"Erro": "Id inválido"})
            return

        # procura em LIVROS o livro com o id procurado e exclui ele da lista e retorna "no content"
        for index, livro in enumerate(LIVROS):
            if livro["id"] == id_livro:
                LIVROS.pop(index)
                self._send_json(204)
                return

        self._send_json(404, {"Erro": "Livro não encontrado"})

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