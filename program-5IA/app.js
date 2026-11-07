const express = require('express')
const userRoutes = require('./routes/userRoutes')
const app = express();
app.use(express.json())
app.use('/user', userRoutes)
app.listen(3000, () => {
    console.log("Serving at port 3000")
})