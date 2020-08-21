# Suffolk County District Attorney API

## Current Status 
The API is currently setup with a single form as an example of how the rest will look. Basics tests 
have been setup but are still being completed(code coverage is very low right now). 

The current test form, a criminal complaint form(called a ccf or cc in the code) features an upload route
to upload the document and get a tracking ID to follow the progress of the processing. Records can be 
retrieved from the `/records` endpoint -- along with URLs for uploaded images. All of these routes related
to uploading, viewing and verifying documents are protected by special permission that must be explicitly
granted by a superuser(even a superuser does not have access to these routes by default).

### API Documentation

The best way to learn about the API is to follow the `domain.name/api/docs` route and view the interactive
swagger documentation for the routes. 

### Frontend access

You can access the frontend, namely the admin dashboard that enables you to edit user permissions via
`domain.name/admin`. Superuser permissions are required to log into this dashboard.

### Account types

As mentioned in the current status section above, there are three types of users. A `user`, a `superuser` and 
`county_authorized`. Anyone can signup and become a `user` but this does not afford them access to any routes.
Meanwhile, a `superuser` has the authorization to edit details(including permissions) of all users. 
`county_authorized` users are the only accounts that have access to routes that interact with the backend
including viewing records, uploading new documents etc. 

In summary: 

- Anyone can signup and has access to only `/api/v1/users/me`
- `county_authorized` users can access `/records` and `/uploads` routes.
- `superuser` users can access `/users` routes which enable them to edit all other users.

### Databases

Both redis and postgres are still being run inside docker and will need to be migrated into AWS.




## Development

The only dependencies for this project should be docker and docker-compose.

### Quick Start

Starting the project with hot-reloading enabled
(the first time it will take a while):

```bash
docker-compose up -d
```

To run the alembic migrations for any database updates:

```bash
docker-compose run --rm backend alembic upgrade head
```

And navigate to http://localhost:8000

_Note: If you see an Nginx error at first with a `502: Bad Gateway` page, you may have to wait for webpack to build the development server (the nginx container builds much more quickly)._

Auto-generated docs will be at
http://localhost:8000/api/docs

### Rebuilding containers:

```
docker-compose build
```

### Restarting containers:

```
docker-compose restart
```

### Bringing containers down:

```
docker-compose down
```

### Frontend Development

Alternatively to running inside docker, it can sometimes be easier
to use npm directly for quicker reloading. To run using npm:

```
cd frontend
npm install
npm start
```

This should redirect you to http://localhost:3000

### Frontend Tests

```
cd frontend
npm install
npm test
```

## Migrations

Migrations are run using alembic. To run all migrations:

```
docker-compose run --rm backend alembic upgrade head
```

To create a new migration:

```
alembic revision -m "create users table"
```

And fill in `upgrade` and `downgrade` methods. For more information see
[Alembic's official documentation](https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script).

## Testing

There is a helper script for both frontend and backend tests:

```
./scripts/test.sh
```

### Backend Tests

```
docker-compose run backend pytest
```

any arguments to pytest can also be passed after this command

### Frontend Tests

```
docker-compose run frontend test
```

This is the same as running npm test from within the frontend directory

## Logging

```
docker-compose logs
```

Or for a specific service:

```
docker-compose logs -f name_of_service # frontend|backend|db
```

## Project Layout

```
backend
└── app
    ├── alembic
    │   └── versions # where migrations are located
    ├── api
    │   └── api_v1
    │       └── endpoints
    ├── core    # config
    ├── db      # db models
    ├── tests   # pytest
    └── main.py # entrypoint to backend

frontend
└── public
└── src
    ├── components
    │   └── Home.tsx
    ├── config
    │   └── index.tsx   # constants
    ├── __tests__
    │   └── test_home.tsx
    ├── index.tsx   # entrypoint
    └── App.tsx     # handles routing
```
