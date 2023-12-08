# Fairfax County Virginia (Court Info) API


## Current Status
The API is currently set up with multiple forms uploaded as an example of how the rest will look. Basics tests have been set up but are still being completed.


The current test form, a demographic defendant information form(called a ddi in the code) features an upload route to upload the documents and get a tracking ID to follow the progress of the processing. Records can be retrieved from the `/api/api_v1/uploads` endpoint -- along with URLs for uploaded images. All of these routes related to uploading, viewing, verifying documents, and retrieving the status of text-parsing by using the Azure OCR parsing tool. 


## Major Items that need updating/TODO


This is a hopefully exhaustive list of all the technical debts that have crept into this project and have not been fixed yet.


- Background Task Errors: Currently the background task is not giving the correct feedback when calling the OCR/Azure tasks. The current workaround is to directly call the OCR without using a background task to create it. 
- There is still a disconnect between retrieving information from Azure and uploading it to the database. CRUD functionality is not fully tested any may be buggy.
- Fully flesh out the database and begin the implementation of the retrieval feature (this will need to be integrated with the frontend)
- Feature of scanned documents retrieval from database. Backend task includes the update of `records`. Frontend tasks include the creation of a provider for retrieving documents from the corresponding api, updating the scanned document list shown on the home page, and fetching the most up-to-date status of the scanned ducuments. 


### API Documentation


The best way to learn about the API is to follow the `domain.name/api/docs` route and view the interactive swagger documentation for the routes.


### Account types


As mentioned in the current status section above, there are three types of users. A `user`, a `superuser` and
`county_authorized`. Anyone can sign up and become a `user` but this does not afford them access to any routes.
Meanwhile, a `superuser` has the authorization to edit details(including permissions) of all users.
`county_authorized` users are the only accounts that have access to routes that interact with the backend
including viewing records, uploading new documents etc.


In summary:


- Anyone can signup and has access to only `/api/v1/users/me`
- `county_authorized` users can access `/records` and `/uploads` routes.
- `superuser` users can access `/users` routes which enable them to edit all other users.




### CI/CD System


Travis CI runs on the `master` and `dev` branches and will push to CodeDeploy using the built in extension in Travis for performing this action. CodeDeploy then handles deploying the updated code to the correct EC2 instances based on the build flags(`dev`, `prod`) and how machines are tagged(`dev`, `prod`)


CodeDeploy is configured via the `appspec.yml` file located in the root of the project. This specifies the scripts run for each lifecycle event along with the location of deployed files etc(currently set as `\srv\scdao-api`)


> :warning: You will need to reconfigure this connection between Travis and CodeDeploy to whatever repository that will be utilized.


> :warning: You will need to provide Travis with the correct secrets to push to CodeDeploy. Check the docs [here](https://docs.travis-ci.com/user/deployment/codedeploy/)


### Docker Configs


There are four docker compose files that are utilized for various different environments. The commands for production and dev environments are below. You can find examples of their use in the `/scripts` folder.


Dev:
`docker-compose -f docker-compose.yml -f docker-compose.dev.yml up`
Prod:
`docker-compose -f docker-compose.yml -f docker-compose.prod.yml up`


If you are just running things locally you do not need to specify what docker-compose file should be utilized. This is because docker will use the default `docker-compose.yml` and combine it with `docker-compose.override.yml` producing a config that works for running things locally.


It's also important to create and accurately fill in the `.env` file that docker leverages to provide required environment variables to each container. There is a template provided and an example of a local config that should work but is not appropriate for anything where security would be a concern(So anything publicly accessible on the internet).


The one caveat is that you will need an S3 bucket setup even to run things locally. This is because the API will upload the image uploaded via the API to S3 -- if this fails the entire operation also fails.


## Routes Overview


The HTTP routes(and the actions they perform) are all fairly self explanatory but I will expand on this a bit here just to clarify some aspects of how the system is defined to 'flow'.


### Upload routes
The upload routes enable the user to upload specific form types to the API for processing. They return a task ID that can be used to lookup the current status of the task(this for example would be useful to let the user know that processing failed for whatever reason, bad image etc.)


The general flow of these is as follows:
- User uploads file via `HTTP POST`
- File is kept in memory while the following is performed
   - File saved to temporary path named `/uploads/uploaded_files`
   - The text in the file is being read by calling `ocr_read`
   - filename + form type + path returned to the calling function
- Task is sent to Microsoft Azure OCR Parsing tool
   - Image text is extracted
   - Content is verified
   - File uploaded 
   - Object created in database
   - Task status is updated


### Record routes


The record routes are super basic CRUD routes that don't do anything special. They support basic paging and record retrieval but nothing terribly special.


## OCR System
The optical character recognition we use is through Azure Document Intelligence. Essentially, `./app/ocr_sys_v2/ocr_read.py` will call Azure and parse the document using a pretrained model. This will then call `./app/ocr_sys_v2/ddi_schemify.py` which will verify the output and either create a schema or return a fail message. 


## Development


The only dependencies for this project should be docker and docker-compose and the environment variable file.


In a development environment(locally or in AWS) hot reload is enabled for both the frontend
and backend. This means you don't need to restart containers to see your changes. The CLI should print
status updates as the API reboots and applies your changes.


This is **not** the case for code that is run on celery workers. You must reboot the celery worker
so restarts with the new code. This can be done with the following command:


`docker-compose restart worker`


> :warning: If you change code that is run on a celery worker you must restart the docker container! Otherwise
your changes will not be applied.


### Environment Variable Settings


Environment variables are throughout the project for sensitive or environment specific configuration details. They are loaded by docker from the .env file located in the
root of the project directory. A template is provided that lists all the values you must fill out. In addition, there is a "local template"
provided called `.envLocalExample` that is meant to be a working version of the environment variable file ready for local development.


You must set these values for things to compile and run. As mentioned in above sections S3 is still an external dependency so either be alright with
that part of the API not working or setup an S3 resource and configure it correctly for use by the API
### Variable Details
```
# This is the hash key used for hashing all passwords.
HASH_KEY=
# This is the S3 Key
S3_KEY_INTERNAL=
# S3 Secret
S3_SECRET_INTERNAL=
# S3 bucket
S3_BUCKET_NAME=
# Redis DB URL, full with port, url and database number
REDIS_DB_URL=
# Postgres DB url, must include: user, password, port and database name
POSTGRES_URL=
# Required by the postgres image. Should use the same password here as in POSTGRES_URL
POSTGRES_PASSWORD=
```
Inside `./app/ocr_sys_v2`, create a .env file with the following:
```
#GET THESE VARIABLES FROM AZURE
VISION_KEY=
VISION_ENDPOINT=
```


### Quick Start


Starting the project with hot-reloading enabled
(the first time it will take a while):


```bash
docker-compose up -d
```


This command automatically applied the `docker-compose.override.yml` file on top of the base `docker-compose.yml` file. The override file specifies various extra resources that enable local development without the need for hosted services.


To run the alembic migrations for any database updates:


```bash
docker-compose run --rm backend alembic upgrade head
```


And navigate to http://localhost:80


_Note: If you see an Nginx error at first with a `502: Bad Gateway` page, you may have to wait for webpack to build the development server (the nginx container builds much more quickly)._


Auto-generated docs will be at
http://localhost:80/api/docs


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


## Migrations


Database migrations are run using alembic. To run all migrations:


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
   │       └── routers
               └── records
               └── tests
           └── uploads
   ├── core    # config
   ├── crud    # crud functions to upload to db
   ├── db      # db models
   ├── models  # sqlalchemy models
   ├── ocr_sys_v2 # Azure Document Intelligence OCR
   ├── schemas # pydantic schemas
   ├── tests   # pytest
   └── main.py # entrypoint to backend

```
