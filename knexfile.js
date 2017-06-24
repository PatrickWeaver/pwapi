module.exports = {
  /*
  production: {
    client: 'postgresql',
    connection: 'postgres://  :5432/pwapi',
    migrations: {
      directory: __dirname + '/src/server/db/migrations'
    },
    seeds: {
      directory: __dirname + '/src/server/db/seeds'
    }
  },
  */
  development: {
    client: 'postgresql',
    connection: 'postgres://pwapi:' + process.env.DB_PASSWORD + '@localhost:5431/pwapi_dev',
    migrations: {
      directory: __dirname + '/src/server/db/migrations'
    },
    seeds: {
      directory: __dirname + '/src/server/db/seeds'
    }
  },
  test: {
    client: 'postgresql',
    connection: 'postgres://localhost:5431/pwapi_test',
    migrations: {
      directory: __dirname + '/src/server/db/migrations'
    },
    seeds: {
      directory: __dirname + '/src/server/db/seeds'
    }
  }
};
