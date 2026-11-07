const express = require('express')
const router = express.Router();
router.get('/view', (req, res) => {
    res.send("marks view")
});
router.get('/:id', (req, res) => {
    res.send(`Student ID: ${req.params.id} `);
});
module.exports = router