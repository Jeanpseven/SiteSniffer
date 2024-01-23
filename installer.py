import os
import subprocess

def instalar_ngrok():
    try:
        # Tenta instalar ngrok com pip
        subprocess.run(['pip', 'install', 'ngrok'], check=True)
    except subprocess.CalledProcessError:
        try:
            # Tenta instalar ngrok com pip e --break-system-packages se a tentativa anterior falhar
            subprocess.run(['pip', 'install', 'ngrok', '--break-system-packages'], check=True)
        except subprocess.CalledProcessError:
            print("Erro ao instalar ngrok. Certifique-se de ter o pip instalado e tente novamente.")
            exit(1)

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
    try:
        # Tenta instalar localxpose com npm
        subprocess.run(['npm', 'install', '-g', 'localxpose'], check=True)
    except subprocess.CalledProcessError:
        print("Erro ao instalar localxpose. Certifique-se de ter o Node.js e o npm instalados e tente novamente.")
        exit(1)

# Instalação do ngrok com pip
instalar_ngrok()

# Verificação e obtenção do token do ngrok
obter_token_ngrok()

# Instalação do localxpose com npm
instalar_localxpose()

print("Ambiente configurado com sucesso.")
