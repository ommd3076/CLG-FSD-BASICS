const express = require('express');
const router = express.Router();
const { validationResult } = require('express-validator');
const { userValidation } = require('../middleware/validator');
router.post('/register', userValidation, (req, res) => {
const errors = validationResult(req);
if (!errors.isEmpty()) {
return res.status(400).json({ errors: errors.array() });
}
res.send('Validation Successful');
});
module.exports = router;
