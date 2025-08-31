# Blogger's Haven 

A blogging platform built with Django where users can register, log in, and share their stories. Admins can manage posts, categories, and users.


## Features

User registration & authentication
Create, update, delete blog posts
Category-based browsing & search
Responsive UI with Bootstrap / Tailwind
Email notifications (via Gmail SMTP / console backend)

## Installation & Setup

1. Clone the repository
 - git clone  https://github.com/resu-sd/blog_site.git
 - cd blog_site

2. Create a virtual environment
 - python -m venv env
 - source env/bin/activate   # Mac/Linux
 - env\Scripts\activate      # Windows

3. Install dependencies
 - pip install -r requirements.txt


4. Set environment variables
 - Create a .env file in the project root:
 - SECRET_KEY=your_secret_key
 - DEBUG=True
 - EMAIL_HOST_USER=your_email@gmail.com
 - EMAIL_HOST_PASSWORD=your_app_password

5. Run migrations
 - python manage.py migrate

6. Create superuser
 - python manage.py createsuperuser

7. Start development server
 - python manage.py runserver


