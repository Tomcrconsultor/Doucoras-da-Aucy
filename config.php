<?php
// Configurações do site
define('SITE_URL', 'https://docurasdaucy.com.br'); // Seu domínio atual
define('UPLOAD_DIR', $_SERVER['DOCUMENT_ROOT'] . '/images/products/');
define('PRODUCTS_FILE', $_SERVER['DOCUMENT_ROOT'] . '/products.json');

// Configurações de segurança
define('ALLOW_ADMIN_ACCESS', true);
define('ADMIN_USERNAME', 'admin'); // Altere para seu usuário desejado
define('ADMIN_PASSWORD', 'sua_senha_segura'); // Altere para sua senha desejada

// Configurações de contato
define('WHATSAPP_NUMBER', 'seu_numero'); // Exemplo: 5511999999999
define('INSTAGRAM_USER', 'seu_instagram');
define('CONTACT_EMAIL', 'seu_email@docurasdaucy.com.br');

// Configurações de timezone
date_default_timezone_set('America/Sao_Paulo');

// Configurações de erro (desative em produção)
ini_set('display_errors', 0);
error_reporting(E_ALL);

// Funções de utilidade
function sanitize_output($buffer) {
    return htmlspecialchars($buffer, ENT_QUOTES, 'UTF-8');
}

function is_secure() {
    return (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off')
        || $_SERVER['SERVER_PORT'] == 443;
}

// Forçar HTTPS
if (!is_secure() && $_SERVER['HTTP_HOST'] !== 'localhost') {
    $redirect = 'https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI'];
    header('HTTP/1.1 301 Moved Permanently');
    header('Location: ' . $redirect);
    exit();
}
?> 