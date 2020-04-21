# Config registry microservice

TODO: add GitHub Actions badge 

---


<<<<<<< HEAD
The aim of test is to create a simple HTTP service that stores and returns configutations that satisfy  certain conditions.
Since we love automating things, the service should be automatically deployed to kubernetes.
=======
Flask based config registry microservice
>>>>>>> 1765f6b... Initial project structure added

## Configuration

Application **MUST** serve the API on the port defined by the environment variable `SERVE_PORT`.

## Links

<<<<<<< HEAD
When you're finished, please do a pull request to `master` and make sure to write about your approach in the description. One or more of our engineers will then perform a code review. We will ask questions which we expect you to be able to answer. Code review is an important part of our process; this gives you as well as us a better understanding of how working together might be like.

We believe it will take 4 to 8 hours to develop this task, however, feel free to invest as much time as you want.

### Endpoints

Your application **MUST** conform to the following endpoint structure and return the HTTP status codes appropriate to each operation.

Following are the endpoints that should be implemented:

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET`       | `/configs`
| Create | `POST`      | `/configs`
| Get    | `GET`       | `/configs/{name}`
| Update | `PUT/PATCH` | `/configs/{name}`
| Delete | `DELETE`    | `/configs/{name}`
| Query  | `GET`       | `/search?name={config_name}&data.{key}={value}`

#### Query

The query endpoint **MUST** return all configs that satisfy the query argument.

### Configuration

Your application **MUST** serve the API on the port defined by the environment variable `SERVE_PORT`.
The application **MUST** fail if the environment variable is not defined.

### Deployment

The application **MUST** be deployable on a kubernetes cluster. Please provide manifest files and a script that deploys the application on a minikube cluster.

The application **MUST** be accesible from outside the minikube cluster on `PORT=<SERVE_PORT>`

#### Schema

- **Config**
  - Name (string)
  - Data (key:value pairs)

## Rules

- You can use any lanuage / framework / SDK of your choice.
- The API **MUST** return valid JSON and **MUST** follow the endpoints set out above.
- You **SHOULD** write testable code and demonstrate unit testing it
- You can use any testing, mocking libraries provided that you state the reasoning and it's simple to install and run.
- You SHOULD document your code and scripts.
=======
 * [Flask][flask]
 * [Gunicorn][gunicorn]
 
[flask]: https://palletsprojects.com/p/flask/ "Flask | The Pallets Projects"
[gunicorn]: https://gunicorn.org/ "Gunicorn - Python WSGI HTTP Server for UNIX"
>>>>>>> 1765f6b... Initial project structure added
