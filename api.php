<?php
header('Content-Type: application/json');

// Função para ler produtos
function getProducts() {
    $productsFile = 'products.json';
    if (file_exists($productsFile)) {
        return json_decode(file_get_contents($productsFile), true);
    }
    return [];
}

// Função para salvar produtos
function saveProducts($products) {
    file_put_contents('products.json', json_encode($products, JSON_PRETTY_PRINT));
}

// Receber dados do POST
$data = json_decode(file_get_contents('php://input'), true);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if ($data['action'] === 'updateProduct') {
        $products = getProducts();
        $newProduct = $data['product'];
        
        // Procura o produto pelo ID
        $found = false;
        foreach ($products as $key => $product) {
            if ($product['id'] === $newProduct['id']) {
                $products[$key] = $newProduct;
                $found = true;
                break;
            }
        }
        
        // Se não encontrou, adiciona novo
        if (!$found) {
            $products[] = $newProduct;
        }
        
        saveProducts($products);
        echo json_encode(['success' => true]);
        exit;
    }
}

// Se chegou aqui, retorna os produtos
echo json_encode(getProducts());
?> 