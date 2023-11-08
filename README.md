# DRF-Firebase-Mongo

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

FB_WEB_KEY = `YOUR FIREBASE WEB API KEY`

FB_CONFIG_FILE_PATH = `PATH TO FIREBASE CONFIG FILE`

MONGO_DB_NAME = `MONGODB DATABASE NAME`

MONGO_HOST = `MONGODB HOST ADDRESS`

MONGO_USER = `MONGODB USERNAME`

MONGO_PASSWORD = `MONGODB PASSWORD`



## Run Locally

**1] Clone the project**

```bash
  git clone https://github.com/AbhishekBhosale46/DRF-Firebase-Mongo
```

**2] Go to the project directory**

```bash
  cd my-project
```

**3] Install dependencies**

```bash
  pip install -r requirements.txt
```

**4] Configure env variables for Firebase Admin and Mongo DB**

**5] Set up the database**

```bash
  python manage.py migrate
```

**6] Start the development server**

```bash
  python manage.py runserver
```
