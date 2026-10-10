const express = require('express');

const router = express.Router();

// Middleware only for profile routes 
router.use((req, res, next) => {
    console.log('Profile middleware');
    next();
});

router.get('/view', (req, res) => {
    res.send('Student Profile View');
});

router.get('/:id', (req, res) => {
    res.send(`Student Profile ID: ${req.params.id}`);
});

module.exports = router; 