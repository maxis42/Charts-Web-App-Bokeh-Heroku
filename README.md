# Charts-Web-App-Bokeh-Heroku
Bokeh charts deployed on heroku example

https://modelling-lab1-charts.herokuapp.com/

Note: app is deployed on free heroku account, so the first loading may take about 30 seconds

## Pipenv part
1. Create environment with required libraries Pipfile

Clone / create project repository:
```
$ cd myproject
```

Install from Pipfile, if there is one:
```
$ pipenv install
```

Or, add a package to your new project:
```
$ pipenv install <package>
```

This will create a Pipfile if one doesn’t exist. If one does exist, it will automatically be edited with the new package your provided.

Next, activate the Pipenv shell:
```
$ pipenv shell
```

2. Create Pipfile.lock
Pipfile.lock takes advantage of some great new security improvements in pip. By default, the Pipfile.lock will be generated with the sha256 hashes of each downloaded package. This will allow pip to guarantee you’re installing what you intend to when on a compromised network, or downloading dependencies from an untrusted PyPI endpoint.
We highly recommend approaching deployments with promoting projects from a development environment into production. You can use `pipenv lock` to compile your dependencies on your development environment and deploy the compiled Pipfile.lock to all of your production environments for reproducible builds.

## Heroku part
Install the Heroku CLI

If you haven't already, log in to your Heroku account and follow the prompts to create a new SSH public key.
```
$ heroku login
```

Clone the repository
Use Git to clone my-first-app-maxis42's source code to your local machine.
```
$ heroku git:clone -a my-first-app-maxis42
$ cd my-first-app-maxis42
```

Deploy your changes
Make some changes to the code you just cloned and deploy them to Heroku using Git.
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```
