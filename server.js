'use strict';

const express = require("express");
//const pgp = require('pg-promise')();
const http = require("http");
const https = require("https");

const port = 8000;
const app = express();
/*
const connection = {
    host: "localhost",
    port: 5432,
    database: "pwapi",
    user: "postgres",
    password: ""
};
const db = pgp(connection);
*/

function getData(request, response, callback) {

  http.get({
    host: "localhost",
    port: 8000,
    path: "/data.json"
  }, function(res) {
    var body = "";
    res.on("data", function(d) {
      body += d;
    });
    res.on("end", function() {
      callback(request, response, JSON.parse(body));
    });
  });
}

// Public
app.use(express.static('public'));

// Data
var data = {};
data.hello = "world";

function resJSON(request, response, data) {
  response.json(data);
}

// App
app.get('/', function (req, res) {
  getData(req, res, resJSON);
});




app.listen(port);
console.log('Running on http://localhost:' + port);
