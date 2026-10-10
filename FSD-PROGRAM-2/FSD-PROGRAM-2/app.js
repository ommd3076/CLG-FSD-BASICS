const express = require('express');
const app = express();
const logger = require('./middleware/logger');
const userRoutes = require('./routes/userRoutes');

app.use(logger); // Apply middleware globally
app.use('/users', userRoutes); // Mount router

app.listen(3000, () => {
    console.log('Server running at http://localhost:3000');
});