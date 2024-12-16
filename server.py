import http.server
import socketserver
import webbrowser
from pathlib import Path
import os
import json
import uuid
import cgi
from urllib.parse import parse_qs, urlparse

class ProductHandler(http.server.SimpleHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS, PUT')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        # Rota para obter um produto específico
        if self.path.startswith('/get-product/'):
            try:
                # Decodificar a URL para tratar caracteres especiais
                product_id = self.path.split('/get-product/')[-1]
                product_id = product_id.split('?')[0]  # Remover query params se houver
                product_id = product_id.replace('%20', ' ')  # Decodificar espaços
                
                products_file = Path('products.json')
                
                if not products_file.exists():
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Arquivo de produtos não encontrado'}).encode('utf-8'))
                    return
                
                with open(products_file, 'r', encoding='utf-8') as f:
                    products = json.load(f)
                    product = next((p for p in products if p['id'] == product_id), None)
                    
                    if product:
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps(product, ensure_ascii=False).encode('utf-8'))
                    else:
                        self.send_response(404)
                        self.send_header('Content-type', 'application/json')
                        self.send_cors_headers()
                        self.end_headers()
                        self.wfile.write(json.dumps({'error': f'Produto não encontrado: {product_id}'}).encode('utf-8'))
                    return

            except Exception as e:
                print(f"Erro ao buscar produto: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        # Servir arquivos estáticos (incluindo imagens)
        if self.path.startswith('/images/'):
            try:
                file_path = Path(self.path.lstrip('/'))
                if file_path.exists():
                    self.send_response(200)
                    self.send_header('Content-type', self.guess_type(str(file_path)))
                    self.send_cors_headers()
                    self.end_headers()
                    with open(file_path, 'rb') as f:
                        self.wfile.write(f.read())
                    return
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/plain')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(b'File not found')
                    return
            except Exception as e:
                self.send_error(500, str(e))
                return

        if self.path == '/get-products':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_cors_headers()
            self.end_headers()
            
            products_file = Path('products.json')
            if products_file.exists():
                with open(products_file, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode())
            else:
                self.wfile.write(json.dumps([]).encode())
            return
        
        return super().do_GET()

    def do_POST(self):
        if self.path == '/save-product':
            try:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )

                product_id = form.getvalue('id') or str(uuid.uuid4())
                product_name = form.getvalue('name', '')
                product_category = form.getvalue('category', '')
                product_description = form.getvalue('description', '')
                product_price = form.getvalue('price', '0')
                product_serves = form.getvalue('serves', '')
                
                # Processar a imagem
                if 'image' in form:
                    fileitem = form['image']
                    if fileitem.filename:
                        # Criar diretório de imagens se não existir
                        image_dir = Path('images/products')
                        image_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Salvar a imagem
                        file_ext = Path(fileitem.filename).suffix
                        image_path = image_dir / f"{str(uuid.uuid4())}{file_ext}"
                        
                        with open(image_path, 'wb') as f:
                            f.write(fileitem.file.read())
                        
                        image_url = f'/{str(image_path)}'
                else:
                    # Se não houver nova imagem, manter a URL existente
                    products_file = Path('products.json')
                    if products_file.exists():
                        with open(products_file, 'r', encoding='utf-8') as f:
                            products = json.load(f)
                            existing_product = next((p for p in products if p['id'] == product_id), None)
                            image_url = existing_product['imageUrl'] if existing_product else '/images/products/no-image.jpg'
                    else:
                        image_url = '/images/products/no-image.jpg'

                # Processar tamanhos se existirem
                sizes = []
                if form.getvalue('sizes'):
                    sizes_data = json.loads(form.getvalue('sizes'))
                    sizes = [
                        {
                            'name': size.get('name', ''),
                            'price': float(size.get('price', 0)),
                            'serves': size.get('serves', '')
                        }
                        for size in sizes_data
                    ]

                # Criar ou atualizar o produto
                product = {
                    'id': product_id,
                    'name': product_name,
                    'category': product_category,
                    'description': product_description,
                    'imageUrl': image_url
                }

                # Adicionar preço e porções apenas se não houver tamanhos
                if not sizes:
                    product['price'] = float(product_price)
                    product['serves'] = product_serves
                else:
                    product['sizes'] = sizes

                # Salvar no products.json
                products_file = Path('products.json')
                products = []
                if products_file.exists():
                    with open(products_file, 'r', encoding='utf-8') as f:
                        products = json.load(f)
                
                # Atualizar produto existente ou adicionar novo
                product_index = next((i for i, p in enumerate(products) if p['id'] == product_id), None)
                if product_index is not None:
                    products[product_index] = product
                else:
                    products.append(product)

                with open(products_file, 'w', encoding='utf-8') as f:
                    json.dump(products, f, ensure_ascii=False, indent=2)

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps(product, ensure_ascii=False).encode('utf-8'))
                return

            except Exception as e:
                print(f"Erro ao salvar produto: {str(e)}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_cors_headers()
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                return

        self.send_error(404)

    def do_DELETE(self):
        if self.path.startswith('/delete-product/'):
            try:
                product_id = self.path.split('/')[-1]
                
                # Carregar produtos existentes
                products_file = Path('products.json')
                if not products_file.exists():
                    raise Exception('Arquivo de produtos não encontrado')
                
                with open(products_file, 'r', encoding='utf-8') as f:
                    products = json.load(f)
                
                # Encontrar e remover o produto
                product = next((p for p in products if p['id'] == product_id), None)
                if product:
                    # Remover a imagem
                    image_path = Path(product['imageUrl'].lstrip('/'))
                    if image_path.exists() and str(image_path) != 'images/products/no-image.jpg':
                        image_path.unlink()
                    
                    # Remover o produto da lista
                    products = [p for p in products if p['id'] != product_id]
                    
                    # Salvar a lista atualizada
                    with open(products_file, 'w', encoding='utf-8') as f:
                        json.dump(products, f, ensure_ascii=False, indent=2)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_cors_headers()
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
                    return
                
                raise Exception('Produto não encontrado')
                
            except Exception as e:
                self.send_error(500, str(e))
                return
        
        self.send_error(404)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

def main():
    PORT = 8000
    DIRECTORY = Path(__file__).parent

    # Criar diretório de imagens se não existir
    products_dir = DIRECTORY / 'images' / 'products'
    products_dir.mkdir(parents=True, exist_ok=True)

    # Criar arquivo products.json se não existir
    products_file = DIRECTORY / 'products.json'
    if not products_file.exists():
        with open(products_file, 'w', encoding='utf-8') as f:
            json.dump([], f)

    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), ProductHandler) as httpd:
        print(f"""
🌐 Servidor iniciado!

📂 Servindo arquivos de: {DIRECTORY}
🔗 URL Local: http://localhost:{PORT}
���� Painel Admin: http://localhost:{PORT}/admin.html

✨ Dicas:
- Pressione Ctrl+C para parar o servidor
- O site abrirá automaticamente no seu navegador
- As alterações nos arquivos serão visíveis ao recarregar a página
""")

        webbrowser.open(f'http://localhost:{PORT}')

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor finalizado!")

if __name__ == '__main__':
    main() 