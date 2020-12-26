# Home bookkeeping

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->
![GitHub repo size](https://img.shields.io/github/repo-size/scottydocs/README-template.md)

The repository explain the source code of the site https://homebookkeeping.herokuapp.com/.

This site helps to keep home bookkeeping

## Installing

First clone the repository from Github and switch to the new directory:

```bash
$ git clone git@github.com/USERNAME/{{ project_name }}.git
$ cd home_bookkeeping
```

Activate the virtualenv for your project.

Install project dependencies:

```bash
$ pip install -r requirements.txt
```

Create necessary environment variables:

```bash
  $ export DJANGO_SECRET_KEY=<secret_key>
  $ export DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=<google_oauth2_secret>
  $ export DJANGO_SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=<google_oauth2_key>
  $ export DJANGO_EMAIL_HOST_USER=<user_for_mailgun.org>
  $ export DJANGO_EMAIL_HOST_PASSWORD=<user_for_mailgun.org>
  $ export DATABASE_URL=<db_url>
```

Apply the migrations:

```bash
$ python manage.py migrate
```

Create a superuser:

```bash
$ python manage.py createsuperuser
```

You can now run the development server:

```bash
$ python manage.py runserver
```


## Tests

Tests catalog structure:

```bash
home_bookkeeping
└── app_name
    └── tests
        └── tests_*.py
```

Run tests:

```bash
$ python manage.py test
```

## Contact

If you want to contact me you can reach me at sotirr@gmail.com.
