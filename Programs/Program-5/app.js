const express = require('express');
const app = express();
const userRoutes = require('./routes/userRoutes');
app.use(express.json());
app.use('/user', userRoutes);
app.listen(3000, () => {
console.log('Server running at http://localhost:3000');
});
