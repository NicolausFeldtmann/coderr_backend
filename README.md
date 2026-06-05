# coderr_backend

> A modular Python backend for managing service offers, customer orders, and reviews.

![GitHub stars](https://img.shields.io/github/stars/NicolausFeldtmann/coderr_backend?style=for-the-badge&logo=github) ![GitHub forks](https://img.shields.io/github/forks/NicolausFeldtmann/coderr_backend?style=for-the-badge&logo=github) ![GitHub issues](https://img.shields.io/github/issues/NicolausFeldtmann/coderr_backend?style=for-the-badge&logo=github) ![Last commit](https://img.shields.io/github/last-commit/NicolausFeldtmann/coderr_backend?style=for-the-badge&logo=github) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 📑 Table of Contents

- [Description](#description)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Key Dependencies](#key-dependencies)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Contributing](#contributing)

## 📝 Description

coderr_backend is a Python-based backend application designed to power service-oriented platforms and marketplaces. Built on a modular Django architecture, the project provides structured, isolated applications to manage the core entities of a service marketplace, including users, offers, orders, and feedback.

## ✨ Key Features

- **🔑 User Authentication Management** — Handles registration, user sessions, and credentials verification through a dedicated authentication application.
- **💼 Service Offerings Management** — Supports creating, updating, and displaying service offers or listings within the marketplace.
- **📦 Customer Order Tracking** — Manages customer transactions and tracks the state of active and completed orders.
- **⭐ Feedback and Reviews System** — Allows clients to submit reviews and view feedback for completed transactions.
- **🛠️ Modular Django Architecture** — Leverages django-style application structures with manage.py and isolated business domains.

## 🎯 Use Cases

- Developing the backend API for a digital service marketplace where freelancers post offers and buyers place orders.
- Implementing a structured order fulfillment system with integrated customer ratings and feedback.
- Bootstrapping a modular Python-based service portal with ready-made separation between users, listings, and checkout pipelines.

## 🛠️ Tech Stack

- 🐍 **Python**

## ⚡ Quick Start

```bash

# 1. Clone the repository
git clone https://github.com/NicolausFeldtmann/coderr_backend.git

# 2. Create & activate a virtualenv
python -m venv env && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start project
python manage.py runserver
```

## 📦 Key Dependencies

```
asgiref: 3.11.1
Django: 6.0.5
django-cors-headers: 4.9.0
django-filter: 25.2
djangorestframework: 3.17.1
pillow: 12.2.0
sqlparse: 0.5.5
```

## 📁 Project Structure

```
.
├── base_infos_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── customer_order_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── offers_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── filters.py
│   │   ├── paginations.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── pyvenv.cfg
├── requirements.txt
├── reviews_app
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── user_auth_app
    ├── __init__.py
    ├── admin.py
    ├── api
    │   ├── permissions.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 🛠️ Development Setup

### Python
1. Install Python (v3.12+ recommended)
2. Create a virtual environment:
3. Activate the environment:
   - Windows: 
   - Unix/MacOS: 
4. Install dependencies:
5. 5. Start project

- Windows:
```
python -m venv env
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver
```

- Unix/MacOS:
```
python -m venv env
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

## 👥 Contributing

Contributions are welcome! Here's the standard flow:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/NicolausFeldtmann/coderr_backend.git`
3. **Branch**: `git checkout -b feature/your-feature`
4. **Commit**: `git commit -m 'feat: add some feature'`
5. **Push**: `git push origin feature/your-feature`
6. **Open** a pull request

Please follow the existing code style and include tests for new behavior where applicable.

---
*This README was generated with Nicolaus Feldtmann
