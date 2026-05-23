# Smart Prescription System

## Setup

##### Step 1 – Clone the repository:

```sh
git clone https://github.com/sajibsd013/smart_prescription_system_backend.git
```

##### Step 2 – Create a virtual environment and activate it:

```sh
python -m venv myenv
myenv\Scripts\activate
```

##### Step 3 – Install dependencies:

```sh
cd smart_prescription_system_backend
pip install -r requirements.txt
```

##### Step 4 – Create a database & seed data:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py seed_data
```

##### Step 5 – Create an admin username and password:

```sh
python manage.py createsuperuser
```

##### **Step 6 – Create `.env` file from `.env.example`**

Before running the project, copy the `.env.example` file and rename it to `.env`, then update the values as needed:

```sh
cp .env.example .env
```

*(On Windows Command Prompt, you can use `copy .env.example .env` instead.)*
Make sure to set the following variables in your `.env` file:

```
DEBUG=1
ALLOWED_HOSTS=*
SECRET_KEY=django-insecure-!mgrw9uq#ed_ugjxs4sujtxw_x+_26vf=jyidet!l9kgvbwj!5
EMAIL_HOST_USER=YOUR EMAIL USERNAME
EMAIL_HOST_PASSWORD=YOUR EMAIL PASSWORD
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
FRONTEND_HOSTNAME=http://localhost:3000
```


##### Step 7 – Run the project:

```sh
python manage.py runserver
```


Success! You can now access the project at `http://localhost:8000`.


## API Documentation
You can find the Postman API documentation for this project at the following link:
[Smart Prescription System Backend API Documentation](https://documenter.getpostman.com/view/21096810/2sB3QMKULj)

