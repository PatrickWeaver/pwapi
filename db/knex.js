var environment = process.env.NODE_ENV;
if (!environment) {
  environment = "development";
}
console.log("**");
console.log(environment);
const config = require('../knexfile.js')[environment];
console.log(config);
module.exports = require('knex')(config);
