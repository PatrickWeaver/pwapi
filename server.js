'use strict';

const express = require('express');
const pgp = require('pg-promise')();

// Constants
const port = 8000;
const app = express();
const connection = {
    host: 'localhost',
    port: 5432,
    database: 'pwapi',
    user: 'postgres',
    password: ''
};
const db = pgp(connection);

// Public
app.use(express.static('public'));

// Data
var data = {};
data.hello = "world";

// App

app.get('/', function (req, res) {
  res.json(data);
});


app.listen(port);
console.log('Running on http://localhost:' + port);
