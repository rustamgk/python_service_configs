# Config registry microservice

---

Flask based config registry microservice with tests, docs adn docker/k8s (minikube) support.

## Usage

### Local dev environment

```shell script
## Create virtualenv
python3 -m virtualenv -ppython3 --no-site-packages venv
## Activate virtualenv
source venv/bin/activate
## Install dev packages
python3 -m pip install -r requirements-dev.txt
## Run tests with tox
#tox
## Run tests
python3 setup.py test 
deactivate
```

### K8s

```shell script
./k8s/k8s-cli.sh build
./k8s/k8s-cli.sh start

## ./k8s/k8s-cli.sh stop
```

### Docker

```shell script
docker-compose up --build
```

## Configuration

Application **MUST** serve the API on the port defined by the environment variable `SERVE_PORT`.

## Docs

 * [Config Registry OpenAPI Spec](./docs/config-registry.openapi.yml)

## Links

 * [OpenAPI][openapi]
 * [Flask][flask]
 * [Gunicorn][gunicorn]
 * [RFC7231][rfc7231]
 
[openapi]: https://swagger.io/specification/
[flask]: https://palletsprojects.com/p/flask/ "Flask | The Pallets Projects"
[gunicorn]: https://gunicorn.org/ "Gunicorn - Python WSGI HTTP Server for UNIX"
[rfc7231]: https://tools.ietf.org/html/rfc7231 "RFC7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content"
[rfc7231-section4.3]: https://tools.ietf.org/html/rfc7231#section-4.3 "RFC7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content. Section 4.3"

