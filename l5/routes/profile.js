const express = require('express')
const router = express.Router();
router.use((req, res, next) => {
    console.log("Profile middle ware")
    next();
});
router.get('/view', (req, res) => {
    res.send("Student view")
});
router.get('/:id', (req, res) => {
    res.send(`stud id: ${req.params.id}`)
});
module.exports = router