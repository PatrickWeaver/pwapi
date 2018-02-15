# PW API

Version: 0.0.13

Python 3.6

Django 1.11.2

## Set Up:

### Required ENV variables:

- DBNAME=[db name]
- DBUSER=[db user]
- DBPASS=[db pass for above user]
- DBHOST=db [or network ip if not using docker-compose]
- ENV=production
- SECRET_KEY=[secret key]
- HOSTS=api.patrickweaver.xyz [or url]


## API Endpoints

### Blog:

- See All Posts: `/blog/posts`
    - Paginated by 5
    - `blog/posts?page=2`
- New Post: `/blog/posts/new`
    ``` python
    from datetime import datetime
    n = datetime.now()
    from blog.models import Post
    p1 = Post(title="First Post", body="This is the first post.\nThere will be more posts later.", post_date=n, created_date=n)
    p1.save()
    ```
