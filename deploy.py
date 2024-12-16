import ftplib
import os
from pathlib import Path
import configparser

def load_config():
    """Carrega as configurações do arquivo config.ini"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    return {
        'host': config['FTP']['host'],
        'user': config['FTP']['user'],
        'password': config['FTP']['password'],
        'directory': config['FTP']['directory']
    }

def upload_file(ftp, local_path, remote_path):
    """Upload de um arquivo para o servidor FTP"""
    with open(local_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_path}', file)
    print(f'✅ Arquivo enviado: {remote_path}')

def upload_directory(ftp, local_dir, remote_dir):
    """Upload de um diretório inteiro para o servidor FTP"""
    local_path = Path(local_dir)
    
    # Lista todos os arquivos e diretórios
    for item in local_path.rglob('*'):
        # Pula arquivos/diretórios que começam com . e arquivos de configuração
        if any(part.startswith('.') for part in item.parts) or \
           item.name in ['config.ini', 'deploy.py']:
            continue
            
        # Caminho relativo para o servidor
        relative_path = item.relative_to(local_path)
        remote_path = f"{remote_dir}/{str(relative_path).replace(os.sep, '/')}"
        
        if item.is_file():
            # Cria diretórios necessários
            current_dir = ''
            for part in str(relative_path.parent).split(os.sep):
                if part:
                    current_dir += f'/{part}'
                    try:
                        ftp.mkd(f"{remote_dir}{current_dir}")
                    except:
                        pass
            
            # Faz upload do arquivo
            upload_file(ftp, str(item), remote_path)

def main():
    print("🚀 Iniciando deploy para HostGator...")
    
    try:
        # Carrega configurações
        config = load_config()
        
        # Conecta ao servidor FTP
        ftp = ftplib.FTP(config['host'])
        ftp.login(config['user'], config['password'])
        print("✅ Conectado ao servidor FTP")
        
        # Muda para o diretório correto
        try:
            ftp.cwd(config['directory'])
        except:
            print(f"⚠️ Diretório {config['directory']} não encontrado")
            return
        
        # Upload de todos os arquivos
        upload_directory(ftp, '.', '')
        
        # Fecha conexão
        ftp.quit()
        print("✅ Deploy concluído com sucesso!")
        
    except configparser.Error:
        print("❌ Erro ao ler arquivo de configuração. Verifique se o arquivo config.ini está correto.")
    except Exception as e:
        print(f"❌ Erro durante o deploy: {str(e)}")

if __name__ == "__main__":
    main() 