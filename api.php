<?php
require_once 'config.php';

// Verificar autenticação para rotas administrativas
function checkAuth() {
    if (!ALLOW_ADMIN_ACCESS) {
        header('HTTP/1.1 403 Forbidden');
        exit('Acesso negado');
    }
}

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, DELETE');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

$request_method = $_SERVER['REQUEST_METHOD'];
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);

// Funções auxiliares
function saveImage($file) {
    $upload_dir = $_SERVER['DOCUMENT_ROOT'] . '/images/products/';
    
    // Criar diretório se não existir
    if (!file_exists($upload_dir)) {
        mkdir($upload_dir, 0755, true);
    }
    
    $file_extension = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $allowed_extensions = ['jpg', 'jpeg', 'png', 'gif'];
    
    if (!in_array($file_extension, $allowed_extensions)) {
        throw new Exception('Tipo de arquivo não permitido');
    }
    
    $new_filename = uniqid() . '.' . $file_extension;
    $target_file = $upload_dir . $new_filename;
    
    if (move_uploaded_file($file['tmp_name'], $target_file)) {
        return '/images/products/' . $new_filename;
    }
    
    throw new Exception('Erro ao salvar imagem');
}

// Rotas da API
switch ($request_method) {
    case 'GET':
        if (strpos($uri, '/get-products') !== false) {
            if (file_exists(PRODUCTS_FILE)) {
                echo file_get_contents(PRODUCTS_FILE);
            } else {
                echo json_encode([]);
            }
        }
        elseif (preg_match('/\/get-product\/(.+)/', $uri, $matches)) {
            $product_id = $matches[1];
            if (file_exists(PRODUCTS_FILE)) {
                $products = json_decode(file_get_contents(PRODUCTS_FILE), true);
                $product = array_filter($products, function($p) use ($product_id) {
                    return $p['id'] === $product_id;
                });
                if (!empty($product)) {
                    echo json_encode(reset($product));
                } else {
                    http_response_code(404);
                    echo json_encode(['error' => 'Produto não encontrado']);
                }
            }
        }
        break;

    case 'POST':
        if ($uri === '/save-product') {
            try {
                $product_data = $_POST;
                $products = [];
                
                if (file_exists(PRODUCTS_FILE)) {
                    $products = json_decode(file_get_contents(PRODUCTS_FILE), true) ?: [];
                }

                if (empty($product_data['id'])) {
                    $product_data['id'] = uniqid();
                }

                // Processar imagem
                if (isset($_FILES['image']) && $_FILES['image']['error'] === 0) {
                    $image_url = saveImage($_FILES['image']);
                    if ($image_url) {
                        $product_data['imageUrl'] = $image_url;
                    }
                }

                // Processar tamanhos
                if (isset($product_data['sizes'])) {
                    $product_data['sizes'] = json_decode($product_data['sizes'], true);
                }

                // Converter preço para float
                if (isset($product_data['price'])) {
                    $product_data['price'] = floatval($product_data['price']);
                }

                // Atualizar ou adicionar produto
                $product_index = array_search($product_data['id'], array_column($products, 'id'));
                if ($product_index !== false) {
                    // Manter a URL da imagem se não foi enviada uma nova
                    if (!isset($product_data['imageUrl'])) {
                        $product_data['imageUrl'] = $products[$product_index]['imageUrl'];
                    }
                    $products[$product_index] = $product_data;
                } else {
                    $products[] = $product_data;
                }

                // Salvar no arquivo
                if (file_put_contents(PRODUCTS_FILE, json_encode($products, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE))) {
                    echo json_encode($product_data);
                } else {
                    throw new Exception('Erro ao salvar produto');
                }
            } catch (Exception $e) {
                http_response_code(500);
                echo json_encode(['error' => $e->getMessage()]);
            }
        }
        break;

    case 'DELETE':
        if (preg_match('/\/delete-product\/(.+)/', $uri, $matches)) {
            try {
                $product_id = $matches[1];
                if (file_exists(PRODUCTS_FILE)) {
                    $products = json_decode(file_get_contents(PRODUCTS_FILE), true);
                    
                    $product_index = array_search($product_id, array_column($products, 'id'));
                    if ($product_index !== false) {
                        // Remover imagem antiga
                        $image_url = $products[$product_index]['imageUrl'];
                        $image_path = $_SERVER['DOCUMENT_ROOT'] . $image_url;
                        if ($image_url && file_exists($image_path)) {
                            unlink($image_path);
                        }
                        
                        array_splice($products, $product_index, 1);
                        file_put_contents(PRODUCTS_FILE, json_encode($products, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));
                        echo json_encode(['success' => true]);
                    } else {
                        http_response_code(404);
                        echo json_encode(['error' => 'Produto não encontrado']);
                    }
                }
            } catch (Exception $e) {
                http_response_code(500);
                echo json_encode(['error' => $e->getMessage()]);
            }
        }
        break;

    case 'OPTIONS':
        header('Access-Control-Allow-Origin: *');
        header('Access-Control-Allow-Methods: GET, POST, DELETE, OPTIONS');
        header('Access-Control-Allow-Headers: Content-Type, Authorization');
        exit(0);
        break;
}
?> 