# Switch

Switch is an online marketplace for students to buy/sell books within educational institutes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip3 install -r requirements.txt
```

## Usage

```python
python3 run.py
```

## The Idea
I found it difficult to buy used books and sell off my old books, so I made this platform to connect with other students who might have what I need.<br>
Many students in my campus struggle with this, so this was one of the solutions.

## Technologies Used
- Python 3
- Flask Server
- SQLite database
- SQLALchemy
- NGINX
- Gunicorn
- HTML
- CSS
- JS
- Jinja

## Features
* Forgot Password
* Pagination
* Templates
* SQLAlchemy for quick deployement
* Create and Update Adverts
* Package structure

## File structure
```
├── forum
│   ├── config.py
│   ├── errors
│   │   ├── handlers.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── models.py
│   ├── posts
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── utils.py
│   ├── site.db
│   ├── static
│   │   ├── anger.png
│   │   ├── books.jpg
│   │   ├── dog.jpeg
│   │   ├── favicon.ico
│   │   ├── fontawesome.min.css
│   │   ├── form.css
│   │   ├── main.css
│   │   ├── panda.jpg
│   │   ├── post_pics
│   │   ├── profile_pics
│   │   │   └── default-dp.jpg
│   │   └── switch.png
│   ├── templates
│   │   ├── about.html
│   │   ├── account.html
│   │   ├── create_post.html
│   │   ├── errors
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── home.html
│   │   ├── layout.html
│   │   ├── login.html
│   │   ├── post.html
│   │   ├── register.html
│   │   ├── reset_request.html
│   │   ├── reset_token.html
│   │   ├── signup.html
│   │   └── user_posts.html
│   └── users
│       ├── forms.py
│       ├── __init__.py
│       ├── routes.py
│       └── utils.py
├── README.md
├── requirements.txt
└── run.py

10 directories, 44 files
```
## Challenges Faced
* CSS - Countless hours were spent on this
* JS - Had to watch a lot of tutorials to get a hang of Javascript
* Databases - I jumped a lot from different SQL versions till I settled on SQLAlchemy and SQLite 
* Pagination and Package structuring - Thanks to some youtubers, I got a pretty good explanation about these. Special Thanks to [Corey Schafer](https://www.youtube.com/user/schafer5).

## Future Scope
* Complete overhaul of the frontend with Ajax and JS.
* Private messages
* Better email and password assistance
* Search and Tags
* Detailed location based adverts


