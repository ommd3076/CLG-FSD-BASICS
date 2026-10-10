const express = require('express');
const app = express();
const collegeRouter = require('./routes/college');
app.use('/college', collegeRouter)
app.listen(3000, () => {
    console.log('Server is running on port 3000');
});