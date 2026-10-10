const express = require('express');
const rateLimit = require('express-rate-limit');
const app = express();

app.use(express.static('public'));

const limiter = rateLimit({
    windowMs: 1 * 60 * 1000,
    max: 5,
    message: 'Too many requests, please try again later.'
});

app.use(limiter);

app.get('/hello', (req, res) => {
    res.send('Hello Express.js');
});

app.use((req, res) => {
    res.status(404).send('Page Not Found');
});

app.listen(3000, () => {
    console.log('Server running at http://localhost:3000');
});