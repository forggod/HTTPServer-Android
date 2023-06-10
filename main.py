import http.server
import socketserver
import json

PORT = 5050
IP = '192.168.0.105'


def read_json():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def write_json(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)


class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            paths = self.path.split('/')
            # Определяем заголовки ответа
            if self.path == '/university':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Создаем и отправляем JSON-ответ
                data = read_json()[paths[1]]
                print(data)
                json_data = json.dumps(data)
                self.wfile.write(json_data.encode())

            elif self.path == '/university/faculties' or \
                    self.path == '/university/groups' or \
                    self.path == '/university/students':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                data = read_json()[paths[1]][paths[2]]
                json_data = json.dumps(data)
                print(json_data)
                self.wfile.write(json_data.encode())

            else:
                self.send_error(404, 'No resource on that address')

        except Exception as e:
            self.send_error(404, str(e))

    def do_POST(self):
        try:
            if self.path == '/university/faculties' or \
                    self.path == '/university/groups' or \
                    self.path == '/university/students':
                paths = self.path.split('/')
                # Получаем данные тела запроса
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                # Обрабатываем данные и сохраняем в файл
                data = read_json()
                data[paths[1]][paths[2]] = json.loads(post_data.decode())
                write_json(data)
                print(json.dumps(data))

                # Определяем заголовки ответа
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                # Создаем и отправляем JSON-ответ
                message = {"message": "Data saved succesfully"}
                json_data = json.dumps(message)
                self.wfile.write(json_data.encode())
            else:
                self.send_error(404, 'No resource on that address')

        except Exception as e:
            self.send_error(404, str(e))


handler = MyHandler
with socketserver.TCPServer((IP, PORT), handler) as httpd:
    print(f'Server was started on {IP}:{PORT}')
    httpd.serve_forever()
