'use strict';

const express = require("express");
const http = require("http");
const https = require("https");

const knex = require("./db/knex");

const port = 8000;
const app = express();



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

function resJSON(request, response, data) {
  response.json(data);
}

// App
app.get('/', function (req, res) {
  //getData(req, res, resJSON);
  knex("posts").select("*")
  .then((posts) => {
    res.status(200).json({
      status: "success",
      data: posts
    });
  })
  .catch((err) => {
    res.status(500).json({
      status: "error",
      data: err
    });
  });
});

app.listen(port);
console.log('Running on http://localhost:' + port);
