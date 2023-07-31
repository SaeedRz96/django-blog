
# Django Blog [for educational purposes]

A Social network for blog lovers. 

Define your blog, add authors, and start writing!

Make an account, follow blogs or topics, and start reading!


## Features

- Create blogs
- Write posts
- Comment
- Like posts
- Many blogs, many authors
- Private blogs
- Private posts
- Subscribe to blogs for new posts
- Save posts to read later
- Tag on posts
- Follow tags
- Series(many posts as a series, like a playlist on youtube)
- Badges for users(like: GoldenPen2023) 
- Report abuse comments, posts, blogs, or users
- Save posts as drafts on not published


## Installation

Clone project in your directory

```bash
  git clone https://github.com/SaeedRz96/django-blog
  cd django-blog
```
Make an environment and install dependencies

```
python3 -m venv my_env
source my_env/bin/activate
pip install -r requirements.txt
```

Create ```.env```  file in same directory as ```settings.py```:

```
SECRET_KEY = <YOUR_SECRET_KEY>
DATABASE_NAME = <YOUR_POSTGRE_DATABASE_NAME>
DATABASE_USER = <YOUR_POSTGRE_USER_NAME>
DATABASE_PASS = <YOUR_POSTGRE_PASSWORD>
ALLOWED_HOSTS = <SET_ALLOWED_HOSTS>
```

Or if you want to use SQLite as your database, simply adjust ```settings.py```

Then just go throw and run the Django server

```
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```
## Contributing

Contributions are always welcome!

Clone this repository, make your changes, and send your pull request.

#### Also, if you develop any frontend project for that, drop an issue to list your repository in the section below for the educational purposes 


## Django blog frontend

Here we have some frontend projects that used this repo as a backend 

-
Nothing still, wait for it!
