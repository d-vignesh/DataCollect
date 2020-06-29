This repo contains the rest api's that allows the user to stop, terminate and resume the file upload and file download process initiated.

Docker image : vickee/datacollect:v2
Docker hub url of docker image: https://hub.docker.com/repository/docker/vickee/datacollect

The repo also contains the configuration file for deployment(deployment.yaml) that can used to deploy the application to kubernetes
command to deploy the application : kubectl apply -f deployment.yaml

The repo also contains the configuration file for service(service.yaml) that can be create a service to access the application.
command to create the service : kubectl apply -f service.yaml

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ee70573e05bd7e0c3b02)