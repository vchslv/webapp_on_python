# ip-adress + port = socket
import socket
from view import *

# using urls
URLS = {
    #'/': 'hi index',
    #'/blog': 'hi blog'
    '/': index,
    '/blog': blog
}

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    url = parsed[1]
    return (method, url)

def generate_headers(method, url):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
        # если ключа нет в словаре
    if not url in URLS:
        return ('HTTP/1.1 404 Not found\n\n', 404)
    return ('HTTP/1.1 200 OK\n\n', 200)

def generate_content(code, url):
    if code == 404:
        return '<h1>404</h1><p>Not found</p>'
    if code == 405:
        return '<h1>405</h1><p>Method not allowed</p>'
    #return '<h1>{}</h1>'.format(URLS[url])
    # call view function
    return URLS[url]()

# generate response
def generate_response(request):
    # распарсить request
    method, url = parse_request(request)
    headers, code = generate_headers(method, url)
    #generate body html page
    body = generate_content(code, url)
    return (headers + body).encode()

def run():
    # принимает request, AF_INET - global variable (family of adress) - IP4-protocol, SOCK_STREAM - TCP-protocol
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # для обхода защитного механищма TCP. SOL_SOCKET - указание на наш сокет, SO_REUSEADDR - допустить повторое using of address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # cвязать субъекта с конкретным адресом и портом
    server_socket.bind(('localhost', 5000))
    # указание серверу - listen port
    server_socket.listen()

    while True:
        # для того, чтобы сервер что-то получил. clint_socket, addr - тот, кто шлет запрос
        client_socket, addr = server_socket.accept()
        request = client_socket.recv(1024)
        print(request)
        print()
        print(addr)

        response = generate_response(request.decode('utf-8'))

        # send response that was преобразован в byte
        client_socket.sendall(response)
        # в браузере ничего не увидим, пока не закроем соединение
        client_socket.close()


if __name__ == '__main__':
    run()
