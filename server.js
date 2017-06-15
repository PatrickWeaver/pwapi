'use strict';

const express = require('express');

// Constants
var port = 8000;

// Data
var data = {};
data.hello = "world";

// App
const app = express();
app.get('/', function (req, res) {
  res.json(data);
});


app.listen(port);
console.log('Running on http://localhost:' + port);
