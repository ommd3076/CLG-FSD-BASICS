const express = require('express');
const mongoose = require('mongoose');
const app = express();
// Middleware to parse JSON request data
app.use(express.json());
app.set('port', 3000);
// Connect to MongoDB
mongoose.connect('mongodb://127.0.0.1:27017/CollegeDB')
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));
// Define Student schema
const studentSchema = new mongoose.Schema({
    name: String,
    usn: String,
    branch: String,
    semester: Number
});
// Create Student model
const Student = mongoose.model('Student', studentSchema);
// POST: Create a new student
app.post('/students', async (req, res) => {
    try {
        const student = new Student(req.body);
        await student.save();

        res.status(201).json({
            message: 'Student created successfully',
            student: student
        });
    } catch (err) {
        res.status(500).json({
            message: 'Error creating student',
            error: err.message
        });
    }
});
// GET: Read all students
app.get('/students', async (req, res) => {
    try {
        const students = await Student.find();
        res.status(200).json({
            message: 'Students retrieved successfully',
            students: students
        });
    } catch (err) {
        res.status(500).json({
            message: 'Error retrieving students',
            error: err.message
        });
    }
});
// Start server
app.listen(3000, () => { console.log('Server running on port 3000'); });
module.exports = app;
 