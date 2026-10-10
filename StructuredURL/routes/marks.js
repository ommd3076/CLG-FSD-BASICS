const express = require('express');

const router = express.Router();

router.get('/view', (req, res) => {
    res.send('Marks View');
});

router.get('/:id', (req, res) => {
    res.send(`Marks for Student ID: ${req.params.id}`);
});

module.exports = router;