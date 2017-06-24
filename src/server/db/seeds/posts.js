
exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('posts').del()
    .then(function () {
      // Inserts seed entries
      return knex('posts').insert([
        {id: 1, post_title: 'First Post', post_body: 'Hello this is the first post. Hello this is the first post. Hello this is the first post. Hello this is the first post.', post_date: new Date(1387493087235)},
        {id: 2, post_title: 'Second Post', post_body: 'Second post is this one. Second post is this one. Second post is this one. Second post is this one.', post_date: new Date(1497493084235)},
        {id: 3, post_title: 'Third Post', post_body: 'Third post, this is the third post. Third post, this is the third post. Third post, this is the third post. Third post, this is the third post.', post_date: new Date(1508593097235)}
      ]);
    });
};
