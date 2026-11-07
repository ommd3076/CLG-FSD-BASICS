const express = require('express');
const router = express.Router();
const { validationResult } = require('express-validator');
const { userValidation } = require('../middlewear/validator');

router.post('/register', userValidation, (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({
            errors: errors.array()
        });
    }
    res.send("Validation success");
});

// Also support GET if needed for testing in browser:
router.get('/register', userValidation, (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        return res.status(400).json({
            errors: errors.array()
        });
    }
    res.send("Validation success");
});

module.exports = router;
