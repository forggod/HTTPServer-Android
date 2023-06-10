import http.server
import socketserver
import json

PORT = 5050
IP = '192.168.0.105'


def open_json():
    with open('data.json') as file:
        data = json.load(file)
    return data


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Определяем заголовки ответа
        if self.path == '/faculties':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Создаем и отправляем JSON-ответ
            faculties = open_json()['faculties']
            data = {"faculties": faculties}
            json_data = json.dumps(data)
            self.wfile.write(json_data.encode())

    def do_POST(self):
        # Получаем данные тела запроса
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Обрабатываем данные и сохраняем в файл
        data = json.loads(post_data.decode())
        with open('data.json', 'w') as file:
            json.dump(data, file)

        # Определяем заголовки ответа
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Создаем и отправляем JSON-ответ
        message = {"message": "Data saved succesfully"}
        json_data = json.dumps(message)
        self.wfile.write(json_data.encode())


handler = MyHandler
with socketserver.TCPServer((IP, PORT), handler) as httpd:
    print(f'Server was started on {IP}:{PORT}')
    httpd.serve_forever()
