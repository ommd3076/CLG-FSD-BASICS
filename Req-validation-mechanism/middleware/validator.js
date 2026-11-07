const { body } = require('express-validator');

exports.userValidation = [
    body('name').notEmpty().withMessage('Name is required'),
    body('email').isEmail().withMessage('Invalid email format'),
    body('age').isInt({ min: 18 }).withMessage('Age must be at least 18')
];
