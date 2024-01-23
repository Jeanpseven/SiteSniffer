import os

def instalar_ngrok():
    # Comando para instalar o ngrok
    comando_ngrok = 'curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok'

    # Verifica se o ngrok já está instalado
    if os.path.exists('/usr/bin/ngrok'):
        print("Ngrok já está instalado.")
        return

    # Executa o comando de instalação do ngrok
    os.system(comando_ngrok)

def obter_token_ngrok():
    # Verifica se o arquivo de configuração do ngrok existe
    if not os.path.exists(os.path.expanduser('~/.ngrok2/ngrok.yml')):
        print("Você precisa configurar o token do ngrok. Siga os passos abaixo:")
        print("1. Crie uma conta no ngrok em https://dashboard.ngrok.com/signup")
        print("2. Faça login em https://dashboard.ngrok.com/auth e copie seu token.")
        print("3. Execute 'ngrok authtoken SEU_TOKEN' substituindo SEU_TOKEN pelo token copiado.")
        print("4. Reinicie este script após configurar o token.")
        exit(1)

def instalar_localxpose():
    # Comando para instalar o localxpose
    comando_localxpose = 'npm install -g localxpose'

    # Verifica se o localxpose já está instalado
    if os.system('localxpose --version') == 0:
        print("LocalXpose já está instalado.")
        return

    # Executa o comando de instalação do localxpose
    os.system(comando_localxpose)

# Instalação do ngrok
instalar_ngrok()

# Verificação e obtenção do token do ngrok
obter_token_ngrok()

# Instalação do localxpose
instalar_localxpose()

print("Ambiente configurado com sucesso.")
