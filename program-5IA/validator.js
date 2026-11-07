const { body } = require('express-validator');

exports.userValidation = [
    body('name').notEmpty().withMessage('Name is req'),
    body('email').isEmail().withMessage('Invalid email.'),
    body('age').isInt({ min: 18 }).withMessage('req age is 18+')
];
