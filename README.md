# Blog Management System

A full-stack blog management system built with Django and PostgreSQL.

The project provides separate functionality for regular users and administrators. Users can create and manage blog posts, interact with other users' posts, and maintain their profiles. Administrators can manage users, posts, categories, tags, and comments through a custom admin panel.

---

## Features

### User Features

- User registration
- User login and logout
- Forgot password page
- User dashboard
- Create blog posts
- Save posts as drafts
- Publish blog posts
- Edit posts
- Delete posts
- View personal posts
- View personal drafts
- Global blog feed
- Search blog posts
- Categories
- Tags
- Like / unlike posts
- Comment on posts
- Delete own comments
- Post details page
- User profile
- Edit profile
- Change password

### Admin Features

The project includes a custom admin panel for staff/superuser accounts.

- Admin dashboard
- View users
- View user details
- Enable / disable users
- Delete users
- View all posts
- View post details
- Edit posts
- Delete posts
- Publish / unpublish posts
- Manage categories
- Create categories
- Edit categories
- Delete categories
- Manage tags
- Create tags
- Edit tags
- Delete tags
- Manage comments
- Delete comments

> The project uses Django's built-in authentication system. A Django superuser/staff account is used as the administrator for the custom admin panel.

---

## Technologies Used

- Python
- Django
- PostgreSQL
- HTML5
- CSS3
- Bootstrap Icons
- Gunicorn
- WhiteNoise
- Render

---

## Project Structure

```text
BlogManagement/
│
├── BlogManagement/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── authentication/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── blog/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── ...
│
├── admin_panal/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── admin/
│   └── user/
│
├── static/
│   ├── css/
│   ├── images/
│   └── ...
│
├── media/
│
├── build.sh
├── manage.py
├── requirements.txt
└── README.md