import ftplib
import os

print("🔄 Tentando conectar ao servidor FTP...")
try:
    # Tenta conectar
    ftp = ftplib.FTP('ftp.docurasdaucy.com.br')
    print("✅ Servidor encontrado")
    
    # Tenta login
    ftp.login('docurasdaucy@docurasdaucy.com.br', '6kO^7,2[ej$l')
    print("✅ Login bem sucedido!")
    
    # Lista o conteúdo do diretório atual
    print("\n📁 Conteúdo do diretório:")
    files = []
    ftp.dir(files.append)
    for f in files:
        print(f)
    
    # Tenta fazer upload do index.html
    print("\n🔄 Tentando fazer upload do index.html...")
    if os.path.exists("index.html"):
        with open("index.html", "rb") as f:
            ftp.storbinary('STOR index.html', f)
        print("✅ Upload do index.html realizado com sucesso!")
    else:
        print("❌ Arquivo index.html não encontrado no diretório local")
    
    # Lista novamente para confirmar o upload
    print("\n📁 Conteúdo atualizado do diretório:")
    files = []
    ftp.dir(files.append)
    for f in files:
        print(f)
    
    # Fecha conexão
    ftp.quit()
    print("\n✅ Teste concluído com sucesso!")
except Exception as e:
    print(f"❌ Erro: {str(e)}")
    print("\n💡 Detalhes do erro para debug:")
    print(f"Tipo do erro: {type(e).__name__}")
    print(f"Mensagem completa: {str(e)}")
    if hasattr(e, 'args'):
        print(f"Argumentos do erro: {e.args}")