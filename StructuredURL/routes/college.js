const express = require('express');

const router = express.Router();

const studentsRouter = require('./students');
const marksRouter = require('./marks');

// Middleware at /college level 
router.use((req, res, next) => {
    console.log('College middleware:', req.method, req.originalUrl);
    next();
});

router.use('/students', studentsRouter);
router.use('/marks', marksRouter);

module.exports = router; 