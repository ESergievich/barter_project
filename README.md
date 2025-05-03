<div align="center">

<h1>Barter Platform</h1>

<p>
A web platform for item exchange based on a **barter system**. Users can list items they want to trade, browse offers from others, and send exchange proposals.
</p>

<p>

<a href="#about">About</a> •
<a href="#installation">Installation</a>

</p>

</div>

### About

This is a **monolithic Django web application** that allows users to:

- Post and manage barter listings.
- Send and receive exchange proposals.
- Accept or reject trade offers.
- Interact via a user-friendly **web interface** or a **REST API**.

The goal is to simplify the process of exchanging items without using money.

### Features

- ✅ User registration and authentication
- 📦 Create, update, and delete item listings
- 🔍 Search and filter listings by various criteria
- 🔁 Send exchange proposals between users
- ✔️ Accept or reject received proposals

### Technology Stack

* **Django** — High-level Python web framework for rapid development.
* **Django REST Framework (DRF)** — Toolkit for building Web APIs in Django.
* **drf-spectacular** — Generates OpenAPI 3 schema and Swagger documentation for DRF.
* **PostgreSQL** — Robust open-source relational database used for storing application data.
* **psycopg2-binary** — PostgreSQL adapter for Python, used by Django to connect to the database.
* **Faker** — Library for generating fake data for testing and development.

### Installation

Clone the project and navigate to the project directory:

```shell
git clone https://github.com/ESergievich/barter_project.git && cd barter_project && cp .env.template .env
```

Then run the application using Docker Compose:

```shell
docker-compose up
```

The backend server will be available at:
http://localhost:8000

Interactive API documentation will be available at:
http://localhost:8000/api/v1/docs/

#### Generating Test Data

To populate the database with fake users, ads, and proposals for testing:

```shell
python manage.py seed
```

Available flags:

* --users — Number of users to create (default is 10)
* --cleardb — Clear the database before seeding

Example:

```shell
python manage.py seed --users=15 --cleardb
```