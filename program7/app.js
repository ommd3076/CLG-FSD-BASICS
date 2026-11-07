// --- app.js ---
const express = require('express');
const mongoose = require('mongoose');
const app = express();
app.use(express.json());
mongoose.connect('mongodb://127.0.0.1:27017/CollegeDB')
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.log(err));
const studentSchema = new mongoose.Schema({
    name: String,
    usn: String,
    branch: String,
    semester: Number
});
const Student = mongoose.model('Student', studentSchema);
app.put('/students/:usn', async (req, res) => {
    try {
        const student = await Student.findOneAndUpdate(
            { usn: req.params.usn },
            req.body,
            { new: true, runValidators: true }
        );
        if (!student) {
            return res.status(404).json({
                message: 'Student not found'
            });
        }
        res.status(200).json({
            message: 'Student updated successfully',
            student: student
        });
    } catch (err) {
        res.status(500).json({
            message: 'Error updating student',
            error: err.message
        });
    }
});
app.delete('/students/:usn', async (req, res) => {
    try {
        const student = await Student.findOneAndDelete({
            usn: req.params.usn
        });
        if (!student) {
            return res.status(404).json({
                message: 'Student not found'
            });
        }
        res.status(200).json({
            message: 'Student deleted successfully',
            student: student
        });
    } catch (err) {
        res.status(500).json({
            message: 'Error deleting student',
            error: err.message
        });
    }
});
app.listen(3000, () => {
    console.log('Server running on port 3000');
});
module.exports = app;