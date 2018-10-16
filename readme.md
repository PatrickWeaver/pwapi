# PW API

Version: 1.1.4

Python 3.6

Django 2.1.2

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

- See All Posts: `/blog/posts/`
    - Paginated by 5 (default):
        - `blog/posts/?page=2`
    - Quantity per page:
        - `blog/posts/?quantity=10`
        - `blog/posts/?quantity=7&page=2`
- New Post: `/blog/posts/new`
    ``` python
    from datetime import datetime
    n = datetime.now()
    from blog.models import Post
    p1 = Post(title="First Post", body="This is the first post.\nThere will be more posts later.", post_date=n, created_date=n)
    p1.save()
    ```
    - New post POST request should return JSON version of:
    ``` python
    "success": True,
    "title": title,
    "slug": slug,
    "summary": summary,
    "body": body,
    "post_date": post_date
    ```

### Uploads:

- POST request with file:
    - `/uploads/new/`
    - `/blog/uploads/new/`
- Send as `multipart/form-data`
- With these fields:
    - `file`
    - `filename`
    - `uuid`
- uuid will be prepended to filename

### Portfolio:

- List Projects: `GET /v1/portfolio/projects`
- View Project: `GET /v1/portfolio/project/[project-slug]`
- New Project: `POST /v1/portfolio/project/[project-slug`
- Edit Project: `PUT /v1/portfolio/project/[project-slug]`
- Delete Project: `DELETE /v1/portfolio/project/[project-slug]`

Project schema:

```
{
  "api_key": "secret-api-key",
  "name": "Name of Project",
  "slug": "name-of-project",
  "description": "Information about the project that is more descriptive.",
  "start_date": "2018-04-25 12:55",
  "end_date": "2018-05-12 00:00"
  "project_url": "http://www.website.com/project",
  "source_url": "http://www.sourcecontrol.com/project",
  "status_id": "2"
 }
 ```
