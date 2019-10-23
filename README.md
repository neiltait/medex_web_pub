# Medical Examiners Service Case Management System

This respository contains the source code for the Medical Examiners Service CMS, providing the frontend UI and the logic for accessing and processing data from the Medical Examiners Service Data API.

### Table of Contents
* [Project Status](#project-status)
  * [Sandbox](#sandbox)
  * [Staging](#staging)
  * [Production](#production)
* [Development](#development)
  * [Tech Stack](#tech-stack)
  * [Running Local Development](#running-local-development)
    * [Environment Variables](#environment-variables)
    * [Starting the server](#starting-the-server)
    * [Useful Commands](#useful-commands)
  * [Testing](#testing)
    * [Strategy](#strategy)
    * [Testing Commands](#testing-commands)
  * [Branching](#branching)
    * [Naming Conventions](#naming-conventions)
        * [Features](#features)
        * [Bugs](#bugs)
        * [Refactoring](#refactoring)
* [Continuous Integration and Deployment Pipeline](#continuous-integration-and-deployment-pipeline)
  * [Continuous Integration](#continuous-integration)
  * [Continuous Deployment](#continuous-deployment)
  * [Creating A Release](#creating-a-release)
  * [Finishing A Release](#finishing-a-release)

## Project Status

### Sandbox

[![Build Status](https://dev.azure.com/DougMills/medical_examiner_front_end/_apis/build/status/methodsanalytics.medex-cms-sandbox?branchName=master)](https://dev.azure.com/DougMills/medical_examiner_front_end/_build/latest?definitionId=5&branchName=master)

### Staging

[![Build Status](https://dev.azure.com/DougMills/medical_examiner_front_end/_apis/build/status/methodsanalytics.medex-cms-staging?branchName=development)](https://dev.azure.com/DougMills/medical_examiner_front_end/_build/latest?definitionId=13&branchName=development)

### Production

_Environment and pipeline still to be set up_

## Development

### Tech Stack

This project uses the following technologies:

- Python/Django
- jQuery
- SASS
- Docker/Compose

### Running Local Development

#### Environment Variables

Running the project locally requires the following environment variables to be set:

- API_URL - this is the address for the Data API. (Defaults to 'http://localhost:9000')
- CMS_URL - this is the domain the CMS is running on. (Defaults to 'http://localhost:12000')
- OP_DOMAIN - the domain name for the OKTA auth service used in this environment
- OP_ISSUER - the method and the auth service being used to authenticate (Defaults to '/oauth/default')
- OP_ID - the client ID provide by OKTA
- OP_SECRET - the client secret provided by OKTA
- REFRESH_PERIOD - the amount of time between retrieving a refresh token from OKTA (in seconds)
- LOGOUT_IF_IDLE_PERIOD - the amount of time before a forced logout
- REQUIRE_HTTPS - set to False for local development
- SECRET_KEY - set this to an arbitrary string
- STAGE - set to LOCAL/STAGING/TESTING/... to populate stage banner

An additional optional environment variable can be set, LOCAL. This variable can be set to True or False (default), setting it to True will cause the CMS to use its on internal mock API for all requests.

#### Browser Cookies

To access the projects front-end when running the server with LOCAL=True, you need to
add the following (blank) cookie files to the browser you will be using:

`medex_id_token`
`medex_auth_token`

One way these can be easily added to your browser (if you are using chrome),
is to use the ['cookie inspector' extension](https://chrome.google.com/webstore/detail/cookie-inspector/jgbbilmfbammlbbhmmgaagdkbkepnijn?hl=en).
This will add an extra tab to the chrome developer console ('Cookies'), which
lets you view, delete or add cookies. To add the blank cookies listed above,
simply right-click anywhere in the cookie list and select 'Add New Cookie'.

#### Starting the server

The local server can be started by running one of the following commands from the root directory of the project:

To run in docker container:

```
docker-compose up
```

To run directly  on local machine:
```
python manage.py runserver 0.0.0.0:8000
```

#### Useful Commands

There are commands setup in the bin directory of the project, that allow easy use of common commands inside the docker container.

- container - takes you on to the containers command line.
- manage - can be passed arguments to run standard django manage.py commands.
- shell - takes you on to the python shell command line for the project.

### Testing

#### Strategy

The project is developed using the TDD approach, using the unittest module for writing unit tests and selenium for running feature tests.

The target coverage level for the project is:

- &gt;80% coverage for unit testing
- Feature tests for each user feature, covering all probable scenarios.

We are also developing to the PyFlakes and pycodestyle coding standards which are been checked using the Python flake8 package.

#### Testing Commands
_These commands can be used when you are running the code using the docker container_

The unit tests can be run with the 'test' command in the bin directory, or can be run with a coverage report using the 'coverage' command in the bin directory. The generated coverage report can then be viewed by opening the 'index.html' file in the 'htmlcov' directory.

The linter  can be run  with the 'lint' command in the bin directory.

### Branching

Development in this project is following the git-flow development pattern.

When starting a new project feature you should create a new branch named in the correct format for what you are working on (see below for naming conventions)

Once development on the branch is complete, the branch should be pushed to the Github repository and a pull request should be opened against the master branch.

The pull request must be reviewed by at least one of the other developers on the project team. In order for the request to be accepted, there must be unit tests in place for the new code in the feature, the CI pipeline must have passed and the new code must pass a code quality review.

#### Naming conventions

##### Features

Feature branches should be named using the following pattern 'feature/`ticket-id`-`branch-name`'

##### Bugs

Bug fix branches should be named using the following pattern 'bug/`ticket-id`-`branch-name`'

##### Refactoring

Refactoring branches should be named using the following pattern 'refactor/`ticket-id (if exists)`-`branch-name`'

## Continuous Integration and Deployment Pipeline

The continuous integration and deployment pipeline for this project is implemented using Azure DevOps pipelines.

### Continuous Integration

The continuous integration pipeline for the project is defined in yml files in the root of the project, all starting with 'azure-pipelines'.

There are 4 pipelines defined in the project.

#### Development test
_Defined in 'azure-pipelines.yml'_

This pipeline should run on every push to Github from feature, bug and refactor branches. All this pipeline does is run the tests to regression check the new code.

#### Sandbox
_Defined in 'azure-pipelines-sandbox.yml'_

This pipeline should run on every push to Github on the development branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the sandbox container registry.

#### Staging
_Defined in 'azure-pipelines-staging.yml'_

This pipeline should run on every push to Github from a release branch. This pipeline runs the tests and, if they pass, builds a docker container and pushes it to the staging container registry.

#### Production

_Defined in 'azure-pipelines-new-azure-subscription.yml'_


### Continuous Deployment

The continuous deployment pipeline is defined through the Azure DevOps pipeline UI.

There are 3 pipelines setup for the project.

#### Sandbox

The pipeline runs when the sandbox CI pipeline passes, it pulls the container generated by the CI build on to the WebApp server and starts the container.

#### Staging

The pipeline runs when the a new container is pushed to the staging container registry, it pulls the container on to the WebApp server and starts the container.

#### Production

The pipeline runs when the a new container is pushed to the production/UAT container registry, it pulls the container on to the WebApp server and starts the container.

### Releases

Releases of the code are following the major/minor/patch pattern for release numbering.

#### Creating a release

New releases can be generated manually or by using the 'release' command in the bin directory.

##### Manual release process

- update the version number with in the version.txt file
- create a new branch named in the pattern 'release/v`version number`' (e.g. release/v0.0.1)
- push the branch to Github

##### Automated release process

- ensure there are no uncommitted changes in your local repository
- call the 'release' command in the bin directory, passing as a parameter either major/minor/patch.

#### Finishing a release

Once a release has been signed off and deployed to production, you need to:

- merge the release branch into master and to development.
- tag master with the release number at the point it was merged in.
- delete the release branch
