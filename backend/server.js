const express = require('express');// to create web server and handle routes
const multer = require('multer'); // for handling image uploads
const cors = require('cors'); // to accept requests from another origin
const axios = require('axios'); // to make http requests
const fs = require('fs'); // file system for reading the image
var FormData = require('form-data');


const app = express(); //create express app
app.use(cors()); // enable cors for all routes
const upload = multer({ dest: 'uploads/' });

app.post('/process', upload.single('image'), async (req, res) => {
  try {
    const formData = new FormData();
    console.log('formData.getHeaders:', typeof formData.getHeaders);
    formData.append('image', fs.createReadStream(req.file.path));

    const response = await axios.post('http://localhost:8000/process', formData, {
      headers: formData.getHeaders()
    });

    res.json(response.data);
  } catch (err) {
    console.error(err);
    res.status(500).send('Analysis failed');
  }
});

app.listen(5000, () => console.log('Server running on port 5000'));