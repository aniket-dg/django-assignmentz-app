# django-assignmentz-app
Online Assignment Submission App. [Live Preview here](http://assignmentz.pythonanywhere.com/)

## Screenshots

<img src="https://github.com/aniket-dg/django-assignmentz-app/blob/master/screenshots/login.PNG" width="400" height="300">   <img src="https://github.com/aniket-dg/django-assignmentz-app/blob/master/screenshots/student_login.PNG" width="400" height="300">
<img src="https://github.com/aniket-dg/django-assignmentz-app/blob/master/screenshots/student_dashboard.PNG" width= "805">
  <img src="https://github.com/aniket-dg/django-assignmentz-app/blob/master/screenshots/profile.PNG" width="400" height="300">  <img src="https://github.com/aniket-dg/django-assignmentz-app/blob/master/screenshots/assignment_review.PNG" width="400" height="300">

## Installation



```
git clone https://github.com/aniket-dg/assignmentz.git
```
Create a VirtualEnv for Python3 and Activate it

Go to the Project Folder
```
cd assignmentz
```
Install all required Libraries
```
pip install -r requirements.txt
```
## Database Configuration
  1. Create database 'assignmentz' using pgAdmin.

## Environment File
1. Create .env file in root folder (i.e. inside assignmentz/) using vscode terminal or using git bash.
1. Open .env file, Create following 5 variables. 
      <br/>SECRET_KEY = 'create new secret key using online tool' <br/>
      USER = 'your database user name'<br/>
      PASSWORD = 'your database password'<br/>
      EMAIL_HOST_USER = 'your email address for forgot password? method'<br/>
      EMAIL_HOST_PASSWORD = 'your email password'  Note: Please don't provide your Personal mail here in production.<br/>
 2. Save file.
 
 Apply Migrations
```
python manage.py migrate
```
 Create Super User
 Remember your username and password.
```
python manage.py createsuperuser
```

Start the Project
```
python manage.py runserver
```
Go to the [localhost](http://127.0.0.1:8000/)


Add Some data for working properly
  1. Go to [adminPanel](http:127.0.0.1:8000/admin)
  2. Enter your credentials you created in the previous step
  3. Add users for student and teacher resp.
  4. Then add Courses, Students, Teachers, resp.
  
## Your app is ready :)
