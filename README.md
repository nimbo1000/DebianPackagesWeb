# Debian Package Reader

A Flask web server exposing information about software packages of a Debian system. The information of the packages is retrieved from */var/lib/dpkg/status* file.

A demo of the application is available [here](https://polar-inlet-63419.herokuapp.com/).

## Quick Start

1. Clone the project

2. Create a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

4. Run the server:
  ```
  $ python app.py
  ```

5. Go to [http://localhost:5000](http://localhost:5000)


Deploying to Heroku
------

1. Signup or login to [Heroku](https://api.heroku.com/signup)
2. Download the [Heroku Toolbelt](https://toolbelt.heroku.com/)
3. On your command line run `heroku login`
4. Activate your virtualenv
5. The dependencies of the application should be in the *requirements.txt* file.
6. Create a Procfile in the main directory and write the following text into it:

  ```
  web: gunicorn app:app --log-file=-
  ```
7. Create a local Git repository, if there isn't one already:

  ```
  $ git init
  $ git add .
  $ git commit -m "A message for the commit"
  ```
8. Create an app on Heroku:

  ```
  $ heroku create
  ```
9. Push the project to Heroku:

  ```
  $ git push heroku master
  ```
10. View the app through the URL provided from heroku.

