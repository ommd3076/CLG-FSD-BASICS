const express = require('express')
const router = express.Router();
const studentsRouter = require('./students')
const marksRouter = require('./marks')
router.use((req, res, next) => {
    console.log("College middleware")
    next();
});
router.use('/students', studentsRouter)
router.use('/marks', marksRouter)
module.exports = router