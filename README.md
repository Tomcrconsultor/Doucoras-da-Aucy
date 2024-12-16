# Doçuras da Aucy - Site

Site da confeitaria Doçuras da Aucy, desenvolvido com PHP, HTML, CSS e JavaScript.

## Estrutura do Projeto

```
/
├── images/          # Imagens do site
│   └── products/    # Imagens dos produtos
├── admin.html       # Painel administrativo
├── api.php         # API REST
├── config.php      # Configurações
├── index.html      # Página principal
├── products.json   # Banco de dados de produtos
└── style.css       # Estilos CSS
```

## Desenvolvimento

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/docuras-da-aucy.git
cd docuras-da-aucy
```

2. Faça suas alterações

3. Commit e push
```bash
git add .
git commit -m "Descrição das alterações"
git push
```

O deploy será feito automaticamente após o push para a branch main.

## Deploy

O deploy é feito automaticamente via GitHub Actions quando há um push para a branch main.
Para fazer deploy manual:

1. Vá para Actions no GitHub
2. Selecione "Deploy to Hostgator"
3. Clique em "Run workflow"

## Manutenção

- Backups são feitos diariamente
- Logs de erro estão em `/error_log`
- Imagens de produtos em `/images/products`
</rewritten_file> 