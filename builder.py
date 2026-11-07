import os
import json
import subprocess
import pypdf

# 1. Clean code for each program strictly according to manual in docs
CODE_PROG3_FILES = {
    'public/index.html': """<!DOCTYPE html>
<html>
<head>
<title>Express Static Resource Demo</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<h1>Welcome to Express.js</h1>
<p>This page demonstrates static resources.</p>
<img src="image.jpg" width="300">
</body>
</html>""",
    'public/style.css': """body{
font-family: Arial;
text-align: center;
}
h1{
color: blue;
}
p{
color: green;
}""",
    'app.js': """const express = require('express');
const rateLimit = require('express-rate-limit');
const app = express();
app.use(express.static('public'));
const limiter = rateLimit({
windowMs: 1 * 60 * 1000,
max: 5,
message: 'Too many requests, please try again later.'
});
app.use(limiter);
app.get('/hello', (req, res) => {
res.send('Hello Express.js');
});
app.use((req, res) => {
res.status(404).send('Page Not Found');
});
app.listen(3000, () => {
console.log('Server running at http://localhost:3000');
});"""
}

CODE_PROG4_FILES = {
    'routes/college.js': """const express = require('express');
const router = express.Router();
const studentsRouter = require('./students');
const marksRouter = require('./marks');
router.use((req, res, next) => {
console.log('College middleware:', req.method, req.originalUrl);
next();
});
router.use('/students', studentsRouter);
router.use('/marks', marksRouter);
module.exports = router;""",
    'routes/students.js': """const express = require('express');
const router = express.Router();
const profileRouter = require('./profile');
router.use('/profile', profileRouter);
module.exports = router;""",
    'routes/profile.js': """const express = require('express');
const router = express.Router();
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
module.exports = router;""",
    'routes/marks.js': """const express = require('express');
const router = express.Router();
router.get('/view', (req, res) => {
res.send('Marks View');
});
router.get('/:id', (req, res) => {
res.send(`Marks for Student ID: ${req.params.id}`);
});
module.exports = router;""",
    'app.js': """const express = require('express');
const app = express();
const collegeRouter = require('./routes/college');
app.use('/college', collegeRouter);
app.listen(3000, () => {
console.log('Server running on port 3000');
});"""
}

CODE_PROG5_FILES = {
    'middleware/validator.js': """const { body } = require('express-validator');
exports.userValidation = [
body('name').notEmpty().withMessage('Name is required'),
body('email').isEmail().withMessage('Invalid email format'),
body('age').isInt({ min: 18 }).withMessage('Age must be at least 18')
];""",
    'routes/userRoutes.js': """const express = require('express');
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
module.exports = router;""",
    'app.js': """const express = require('express');
const app = express();
const userRoutes = require('./routes/userRoutes');
app.use(express.json());
app.use('/user', userRoutes);
app.listen(3000, () => {
console.log('Server running at http://localhost:3000');
});"""
}

CODE_PROG6_FILES = {
    'app.js': """const express = require('express');
const mongoose = require('mongoose');
const app = express();
app.use(express.json());
app.set('port', 3000);
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
app.listen(3000, () => {
console.log('Server running on port 3000');
});
module.exports = app;"""
}

CODE_PROG7_FILES = {
    'app.js': """const express = require('express');
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
module.exports = app;"""
}

def build_sequential_code(files_dict):
    parts = []
    for filepath, code in files_dict.items():
        parts.append(f"// --- {filepath} ---\n" + code.strip())
    return "\n\n".join(parts)

SEQ_P3 = build_sequential_code(CODE_PROG3_FILES)
SEQ_P4 = build_sequential_code(CODE_PROG4_FILES)
SEQ_P5 = build_sequential_code(CODE_PROG5_FILES)
SEQ_P6 = build_sequential_code(CODE_PROG6_FILES)
SEQ_P7 = build_sequential_code(CODE_PROG7_FILES)

# Commands and Outputs
META = {
    1: {
        "title": "PROGRAM 3: ERROR HANDLING, STATIC RESOURCES AND RATE-LIMITING",
        "short_title": "Prog 3: Static & Rate Limit",
        "cmds": "npm init -y\nnpm install express express-rate-limit\nnode app.js",
        "output": """GET http://localhost:3000/
-> Displays index.html with CSS and image (Status: 200 OK)

GET http://localhost:3000/hello
-> Hello Express.js (Status: 200 OK)

GET http://localhost:3000/xyz
-> Page Not Found (Status: 404 Not Found)

After 5 requests in 1 minute:
-> Too many requests, please try again later. (Status: 429)"""
    },
    2: {
        "title": "PROGRAM 4: HIERARCHICAL ROUTING IN EXPRESS.JS",
        "short_title": "Prog 4: Hierarchical Routing",
        "cmds": "npm init -y\nnpm install express\nnode app.js",
        "output": """GET http://localhost:3000/college/students/profile/view
-> Student Profile View

GET http://localhost:3000/college/students/profile/101
-> Student Profile ID: 101

GET http://localhost:3000/college/marks/view
-> Marks View

GET http://localhost:3000/college/marks/101
-> Marks for Student ID: 101

Console Log Output:
College middleware: GET /college/students/profile/view
Profile middleware"""
    },
    3: {
        "title": "PROGRAM 5: REQUEST VALIDATION USING EXPRESS-VALIDATOR",
        "short_title": "Prog 5: Request Validation",
        "cmds": "npm init -y\nnpm install express express-validator\nnode app.js",
        "output": """POST http://localhost:3000/user/register
Valid JSON: {"name": "John", "email": "john@gmail.com", "age": 25}
Response: Validation Successful (Status: 200 OK)

Invalid JSON: {"name": "", "email": "abc", "age": 15}
Response: Status 400 Bad Request
{"errors": [{"msg": "Name is required"}, {"msg": "Invalid email format"}, {"msg": "Age must be at least 18"}]}"""
    },
    4: {
        "title": "PROG 6: MONGOOSE POST & GET (CREATE & READ)",
        "short_title": "Prog 6: Mongoose POST & GET",
        "cmds": "npm init -y\nnpm install express mongoose\nnode app.js",
        "output": """POST http://localhost:3000/students
Body: {"name": "Rahul", "usn": "4VV23IS001", "branch": "ISE", "semester": 5}
Response (201 Created):
{"message": "Student created successfully", "student": {"_id": "...", "name": "Rahul", "usn": "4VV23IS001", "branch": "ISE", "semester": 5}}

GET http://localhost:3000/students
Response (200 OK):
{"message": "Students retrieved successfully", "students": [{"_id": "...", "name": "Rahul", "usn": "4VV23IS001", "branch": "ISE", "semester": 5}]}"""
    },
    5: {
        "title": "PROG 7: MONGOOSE PUT & DELETE (UPDATE & DELETE)",
        "short_title": "Prog 7: Mongoose PUT & DEL",
        "cmds": "npm init -y\nnpm install express mongoose\nnode app.js",
        "output": """PUT http://localhost:3000/students/4VV23IS001
Body: {"name": "Rahul Kumar", "branch": "CSE", "semester": 6}
Response (200 OK):
{"message": "Student updated successfully", "student": {"_id": "...", "name": "Rahul Kumar", "usn": "4VV23IS001", "branch": "CSE", "semester": 6}}

DELETE http://localhost:3000/students/4VV23IS002
Response (200 OK):
{"message": "Student deleted successfully", "student": {"_id": "...", "name": "xyz", "usn": "4VV23IS002"}}"""
    }
}

# Standalone directory creation
programs_dict = {
    'Program-3': (CODE_PROG3_FILES, {'express': '^4.18.2', 'express-rate-limit': '^7.1.5'}),
    'Program-4': (CODE_PROG4_FILES, {'express': '^4.18.2'}),
    'Program-5': (CODE_PROG5_FILES, {'express': '^4.18.2', 'express-validator': '^7.0.1'}),
    'Program-6': (CODE_PROG6_FILES, {'express': '^4.18.2', 'mongoose': '^8.0.0'}),
    'Program-7': (CODE_PROG7_FILES, {'express': '^4.18.2', 'mongoose': '^8.0.0'}),
}

base_dir = 'Programs'
for prog_name, (files, deps) in programs_dict.items():
    pdir = os.path.join(base_dir, prog_name)
    os.makedirs(pdir, exist_ok=True)
    for rel_path, code in files.items():
        full_path = os.path.join(pdir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(code + '\n')
    pkg = {
        "name": prog_name.lower(),
        "version": "1.0.0",
        "main": "app.js",
        "dependencies": deps
    }
    with open(os.path.join(pdir, 'package.json'), 'w', encoding='utf-8') as f:
        json.dump(pkg, f, indent=2)

print("Created folder structure in Programs/")

# HTML dashboard
html_dashboard = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FSD Lab Programs (3, 4, 5, 6, 7)</title>
<style>
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}
body {{
    background-color: #141414;
    color: #cccccc;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    height: 100vh;
    width: 100vw;
    overflow: hidden;
    user-select: none;
}}
.container {{
    display: grid;
    grid-template-columns: repeat(5, minmax(0, 1fr));
    gap: 5px;
    padding: 5px;
    height: 100vh;
    width: 100vw;
}}
.column {{
    background: #1b1b1b;
    border: 1px solid #2b2b2b;
    border-radius: 3px;
    display: flex;
    flex-direction: column;
    height: 100%;
    min-width: 0;
    overflow: hidden;
}}
.big-btn {{
    width: 100%;
    height: 80px;
    background: #242424;
    border: none;
    border-bottom: 1px solid #333333;
    color: #cccccc;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    padding: 6px 4px;
    transition: background 0.1s ease, color 0.1s ease;
    outline: none;
}}
.big-btn:hover {{
    background: #2e2e2e;
    color: #ffffff;
}}
.big-btn:active {{
    background: #383838;
}}
.big-btn.copied {{
    background: #1e2e22;
    color: #8ae096;
    border-bottom-color: #2e5933;
}}
.num-badge {{
    font-size: 14px;
    font-weight: 700;
    letter-spacing: 0.5px;
    color: #e0e0e0;
}}
.action-label {{
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}}
.meta-desc {{
    font-size: 9px;
    color: #777777;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 95%;
}}
.cmd-strip {{
    background: #181818;
    border-bottom: 1px solid #262626;
    padding: 3px 6px;
    font-family: Consolas, monospace;
    font-size: 8.5px;
    color: #888888;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}
.code-area {{
    flex: 1;
    overflow-y: auto;
    overflow-x: hidden;
    background: #111111;
    padding: 7px;
    cursor: pointer;
    user-select: text;
}}
.code-area::-webkit-scrollbar {{
    width: 4px;
}}
.code-area::-webkit-scrollbar-track {{
    background: #111111;
}}
.code-area::-webkit-scrollbar-thumb {{
    background: #2b2b2b;
    border-radius: 2px;
}}
.code-area::-webkit-scrollbar-thumb:hover {{
    background: #444444;
}}
pre {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 9.5px;
    line-height: 1.22;
    color: #b5b5b5;
    white-space: pre-wrap;
    word-break: break-all;
}}
.output-box {{
    background: #161616;
    border-top: 1px solid #262626;
    padding: 5px 7px;
    max-height: 125px;
    overflow-y: auto;
    font-family: Consolas, monospace;
    font-size: 8.5px;
    line-height: 1.2;
    color: #888888;
    user-select: text;
}}
.output-box::-webkit-scrollbar {{
    width: 3px;
}}
.output-box::-webkit-scrollbar-thumb {{
    background: #333;
}}
.output-title {{
    font-weight: 700;
    font-size: 8.5px;
    color: #aaa;
    margin-bottom: 2px;
}}
#toast {{
    position: fixed;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    background: #252525;
    color: #8ae096;
    border: 1px solid #383838;
    padding: 5px 14px;
    font-size: 11px;
    border-radius: 3px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease;
    z-index: 100;
}}
</style>
</head>
<body>

<div class="container">
"""

for i in range(1, 6):
    html_dashboard += f"""    <!-- COLUMN {i} -->
    <div class="column">
        <button class="big-btn" id="btn-{i}" onclick="copyCode({i})">
            <span class="num-badge">{i}</span>
            <span class="action-label" id="label-{i}">CLICK TO COPY</span>
            <span class="meta-desc">{META[i]['short_title']}</span>
        </button>
        <div class="cmd-strip" title="Run command">{META[i]['cmds'].replace(chr(10), ' &amp;&amp; ')}</div>
        <div class="code-area" title="Click button or press {i} to copy" onclick="copyCode({i})">
            <pre><code id="code-{i}"></code></pre>
        </div>
        <div class="output-box">
            <div class="output-title">OUTPUT / TEST:</div>
            <div>{META[i]['output'].replace(chr(10), '<br>')}</div>
        </div>
    </div>
"""

html_dashboard += f"""</div>

<div id="toast">Copied to clipboard</div>

<script>
const codes = {{
    1: {json.dumps(SEQ_P3)},
    2: {json.dumps(SEQ_P4)},
    3: {json.dumps(SEQ_P5)},
    4: {json.dumps(SEQ_P6)},
    5: {json.dumps(SEQ_P7)}
}};

for (let i = 1; i <= 5; i++) {{
    const el = document.getElementById('code-' + i);
    if (el) el.textContent = codes[i];
}}

let toastTimer = null;
function showToast(msg) {{
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.opacity = '1';
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {{
        toast.style.opacity = '0';
    }}, 1200);
}}

function copyCode(num) {{
    const text = codes[num];
    const btn = document.getElementById('btn-' + num);
    const label = document.getElementById('label-' + num);

    if (navigator.clipboard && window.isSecureContext) {{
        navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
    }} else {{
        fallbackCopy(text);
    }}

    if (btn && label) {{
        btn.classList.add('copied');
        label.textContent = 'COPIED ✓';
        showToast('Program ' + num + ' copied!');
        setTimeout(() => {{
            btn.classList.remove('copied');
            label.textContent = 'CLICK TO COPY';
        }}, 1200);
    }}
}}

function fallbackCopy(text) {{
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    try {{
        document.execCommand('copy');
    }} catch (e) {{}}
    document.body.removeChild(ta);
}}

window.addEventListener('keydown', (e) => {{
    if (['1', '2', '3', '4', '5'].includes(e.key)) {{
        copyCode(parseInt(e.key));
    }}
}});
</script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_dashboard)

with open('programs.html', 'w', encoding='utf-8') as f:
    f.write(html_dashboard)

# 3. PDF HTML template
def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

pdf_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@page {{
    size: A4 portrait;
    margin: 6mm 8mm 6mm 8mm;
}}
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}
body {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 7.2pt;
    line-height: 1.13;
    color: #111111;
    background: #ffffff;
}}
.page {{
    page-break-after: always;
    break-after: page;
    height: 283mm;
    max-height: 283mm;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}}
.page:last-child {{
    page-break-after: avoid;
    break-after: avoid;
}}
.page-title {{
    font-size: 8.5pt;
    font-weight: bold;
    border-bottom: 1.5px solid #222;
    padding-bottom: 2px;
    margin-bottom: 3px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}
.sec-title {{
    font-size: 7.2pt;
    font-weight: bold;
    background: #f0f0f0;
    border-left: 3px solid #444;
    padding: 1px 4px;
    margin-top: 3px;
    margin-bottom: 2px;
    text-transform: uppercase;
}}
pre {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 7pt;
    line-height: 1.12;
    white-space: pre-wrap;
    word-break: break-all;
}}
.p4-pre {{
    font-size: 6.8pt;
    line-height: 1.11;
}}
.box {{
    border: 1px solid #ccc;
    background: #fafafa;
    padding: 3px 5px;
    margin-top: 1px;
    margin-bottom: 3px;
}}
.two-col-container {{
    display: flex;
    flex-direction: row;
    gap: 5mm;
    height: 100%;
}}
.col-half {{
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
}}
.col-half .page-title {{
    font-size: 7.8pt;
}}
.col-half pre {{
    font-size: 6.7pt;
    line-height: 1.11;
}}
.col-half .box {{
    padding: 2px 4px;
    font-size: 6.7pt;
}}
</style>
</head>
<body>

<!-- PAGE 1: PROGRAM 3 -->
<div class="page">
    <div class="page-title">{META[1]['title']}</div>
    <div class="sec-title">COMMANDS TO RUN</div>
    <div class="box"><pre>{escape_html(META[1]['cmds'])}</pre></div>
    <div class="sec-title">SOURCE CODE</div>
    <pre>{escape_html(SEQ_P3)}</pre>
    <div class="sec-title">OUTPUT &amp; TESTING</div>
    <div class="box"><pre>{escape_html(META[1]['output'])}</pre></div>
</div>

<!-- PAGE 2: PROGRAM 4 -->
<div class="page">
    <div class="page-title">{META[2]['title']}</div>
    <div class="sec-title">COMMANDS TO RUN</div>
    <div class="box"><pre>{escape_html(META[2]['cmds'])}</pre></div>
    <div class="sec-title">SOURCE CODE</div>
    <pre class="p4-pre">{escape_html(SEQ_P4)}</pre>
    <div class="sec-title">OUTPUT &amp; TESTING</div>
    <div class="box"><pre>{escape_html(META[2]['output'])}</pre></div>
</div>

<!-- PAGE 3: PROGRAM 5 -->
<div class="page">
    <div class="page-title">{META[3]['title']}</div>
    <div class="sec-title">COMMANDS TO RUN</div>
    <div class="box"><pre>{escape_html(META[3]['cmds'])}</pre></div>
    <div class="sec-title">SOURCE CODE</div>
    <pre>{escape_html(SEQ_P5)}</pre>
    <div class="sec-title">OUTPUT &amp; TESTING</div>
    <div class="box"><pre>{escape_html(META[3]['output'])}</pre></div>
</div>

<!-- PAGE 4: PROGRAM 6 & 7 SIDE BY SIDE -->
<div class="page">
    <div class="page-title" style="margin-bottom: 4px;">PROGRAM 6 &amp; PROGRAM 7: MONGOOSE REST APIS</div>
    <div class="two-col-container">
        <!-- LEFT: PROGRAM 6 -->
        <div class="col-half" style="border-right: 1px dashed #bbb; padding-right: 2.5mm;">
            <div class="page-title" style="border-bottom: 1px solid #777;">{META[4]['title']}</div>
            <div class="sec-title">COMMANDS TO RUN</div>
            <div class="box"><pre>{escape_html(META[4]['cmds'])}</pre></div>
            <div class="sec-title">SOURCE CODE</div>
            <pre>{escape_html(SEQ_P6)}</pre>
            <div class="sec-title">OUTPUT &amp; TESTING</div>
            <div class="box"><pre>{escape_html(META[4]['output'])}</pre></div>
        </div>
        <!-- RIGHT: PROGRAM 7 -->
        <div class="col-half">
            <div class="page-title" style="border-bottom: 1px solid #777;">{META[5]['title']}</div>
            <div class="sec-title">COMMANDS TO RUN</div>
            <div class="box"><pre>{escape_html(META[5]['cmds'])}</pre></div>
            <div class="sec-title">SOURCE CODE</div>
            <pre>{escape_html(SEQ_P7)}</pre>
            <div class="sec-title">OUTPUT &amp; TESTING</div>
            <div class="box"><pre>{escape_html(META[5]['output'])}</pre></div>
        </div>
    </div>
</div>

</body>
</html>
"""

with open('pdf_template.html', 'w', encoding='utf-8') as f:
    f.write(pdf_html)

print("Generated files successfully.")
