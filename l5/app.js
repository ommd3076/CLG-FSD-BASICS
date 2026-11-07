const express = require('express')
const collegeRouter = require('./routes/college')
const app = express();
app.use('/college', collegeRouter)
app.listen(3000, () => {
    console.log("server running on port 3000")
});
