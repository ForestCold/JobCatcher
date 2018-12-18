# JobCatcher

__Try it out! [https://job-catcher.herokuapp.com/](https://job-catcher.herokuapp.com/)__

<img src = "demo.png" width="500" align="middle">

## Development

  ### Environment Requirement
  - Python 2.7
  - pip

  ### Deployment
  - Heroku

  ### Install Heroku Dev CLI

  ```bash
  $ brew install heroku/brew/heroku
  ```

  ### Install **flask**

  ```bash
  $ pip install flask gunicorn
  ```
  ### Set up Web Server

  ```bash
  $ heroku
  ```
  
  ### Run Application

  ```bash
  $ gunicorn app:app  
  ```
