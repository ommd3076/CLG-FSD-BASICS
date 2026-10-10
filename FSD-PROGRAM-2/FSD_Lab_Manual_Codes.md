# Full Stack Development Lab Codes (Part 1: Exp 1-5)

Here are the complete codes and file structures for the first 5 experiments from your syllabus. 

---

## Experiment 1: Basic Setup and Server Test
**Aim:** Setup a web application project using Express.js and run the server.

**Commands to run first:**
```bash
npm init -y
npm install express
```

**`app.js`**
```javascript
const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    res.send('Hello, Express server is working perfectly!');
});

app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
```

---

## Experiment 2: Middleware, Controllers, and Routers
**Aim:** Demonstrate middleware, controllers, and routers.

**Folder Structure:**
```text
/controllers
  └── userController.js
/middleware
  └── logger.js
/routes
  └── userRoutes.js
app.js
```

**`middleware/logger.js`**
```javascript
const logger = (req, res, next) => {
    console.log(`[LOG]: ${req.method} request to ${req.url}`);
    next();
};
module.exports = logger;
```

**`controllers/userController.js`**
```javascript
exports.getUser = (req, res) => {
    res.send('User Controller Executed successfully');
};
```

**`routes/userRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.get('/', userController.getUser);

module.exports = router;
```

**`app.js`**
```javascript
const express = require('express');
const app = express();
const logger = require('./middleware/logger');
const userRoutes = require('./routes/userRoutes');

app.use(logger); // Apply middleware globally
app.use('/users', userRoutes); // Mount router

app.listen(3000, () => {
    console.log('Server running at http://localhost:3000');
});
```

---

## Experiment 3: Error Handling, Static Resources, Rate-Limiting
**Aim:** Implement error handling, static resources, and rate-limiting.

**Commands to run first:**
```bash
npm install express-rate-limit
```

**Folder Structure:**
```text
/public
  └── index.html
app.js
```

**`public/index.html`**
```html
<!DOCTYPE html>
<html>
<head><title>Static Page</title></head>
<body><h1>This is a static HTML resource!</h1></body>
</html>
```

**`app.js`**
```javascript
const express = require('express');
const rateLimit = require('express-rate-limit');
const path = require('path');
const app = express();

// 1. Rate Limiting Middleware
const limiter = rateLimit({
    windowMs: 1 * 60 * 1000, // 1 minute
    max: 5, // limit each IP to 5 requests per window
    message: "Too many requests, please try again after a minute."
});
app.use(limiter);

// 2. Static Resources
app.use(express.static(path.join(__dirname, 'public')));

app.get('/crash', (req, res) => {
    throw new Error('Simulated Server Crash!');
});

// 3. Error Handling (404 Not Found)
app.use((req, res, next) => {
    res.status(404).send('Error 404: Page Not Found');
});

// 4. Error Handling (500 Internal Server Error)
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Error 500: Something broke on the server!');
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
```

---

## Experiment 4: Hierarchical Routing
**Aim:** Design hierarchical routing (e.g., `/college/students` and `/college/marks`).

**Folder Structure:**
```text
/routes
  └── collegeRoutes.js
  └── studentRoutes.js
  └── marksRoutes.js
app.js
```

**`routes/studentRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();

router.get('/profile', (req, res) => res.send('Student Profile Page'));
module.exports = router;
```

**`routes/marksRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();

router.get('/view', (req, res) => res.send('Viewing all marks'));
router.get('/:id', (req, res) => res.send(`Viewing marks for ID: ${req.params.id}`));
module.exports = router;
```

**`routes/collegeRoutes.js`**
```javascript
const express = require('express');
const router = express.Router();
const studentRoutes = require('./studentRoutes');
const marksRoutes = require('./marksRoutes');

// Hierarchical mounting
router.use('/students', studentRoutes);
router.use('/marks', marksRoutes);

module.exports = router;
```

**`app.js`**
```javascript
const express = require('express');
const app = express();
const collegeRoutes = require('./routes/collegeRoutes');

app.use('/college', collegeRoutes);

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
```

---

## Experiment 5: Request Validation
**Aim:** Validate user input (name, email, age) using express-validator.

**Commands to run first:**
```bash
npm install express-validator
```

**`app.js`**
```javascript
const express = require('express');
const { body, validationResult } = require('express-validator');
const app = express();

app.use(express.json()); // Middleware to parse JSON body

app.post('/register', [
    // Validation Middleware rules
    body('name').notEmpty().withMessage('Name is required'),
    body('email').isEmail().withMessage('Valid email is required'),
    body('age').isInt({ min: 18 }).withMessage('Age must be a number and at least 18')
], (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
        // Return errors if validation fails
        return res.status(400).json({ errors: errors.array() });
    }
    
    // Success response
    res.send('User registered successfully! Data is valid.');
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
```
