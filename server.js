const express = require('express');
const path = require('path');

const app = express();

app.use('/images', express.static('images'));

// Middleware para tratar imagens não encontradas
app.use((req, res, next) => {
    if (req.url.match(/\.(jpg|jpeg|png|gif)$/) && res.statusCode === 404) {
        res.sendFile(path.join(__dirname, 'images', 'products', 'no-image.jpg'));
    } else {
        next();
    }
});

// ... existing code ...

app.listen(3000, () => {
    console.log('Server is running on port 3000');
}); 