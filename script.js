function fazerPedido(produto, seletorId = null) {
    const telefone = '5587981334968';
    let tamanho = '';
    
    if (seletorId) {
        // Pega o tamanho selecionado do select
        const select = document.getElementById(seletorId);
        tamanho = select.value;
    } else {
        // Para produtos com tamanho único
        const card = document.querySelector(`.product-card:has(h3:contains("${produto}"))`);
        if (card) {
            const sizeInfo = card.querySelector('.single-size');
            if (sizeInfo) {
                const size = sizeInfo.querySelector('.size').textContent;
                const price = sizeInfo.querySelector('.price').textContent;
                tamanho = `${size} - ${price}`;
            }
        }
    }
    
    const mensagem = `Olá! Gostaria de fazer um pedido do cardápio de Natal:

${produto}${tamanho ? `\nTamanho: ${tamanho}` : ''}

Poderia me ajudar?`;
    
    const mensagemCodificada = encodeURIComponent(mensagem);
    const urlWhatsapp = `https://wa.me/${telefone}?text=${mensagemCodificada}`;
    
    window.open(urlWhatsapp, '_blank');
}

// Adiciona animação suave ao scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Animação de fade-in aos elementos quando aparecem na tela
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in');
        }
    });
}, {
    threshold: 0.1
});

document.querySelectorAll('.combo-card, .product-card, .info-card').forEach((element) => {
    observer.observe(element);
}); 