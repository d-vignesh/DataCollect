This repo contains the rest api's that allows the user to stop, terminate and resume the file upload and file download process initiated.

Docker image : vickee/datacollect:v2 <br />
Docker hub url of docker image: https://hub.docker.com/repository/docker/vickee/datacollect

The repo also contains the configuration file for deployment(deployment.yaml) that can used to deploy the application to kubernetes <br />
command to deploy the application : kubectl apply -f deployment.yaml

The repo also contains the configuration file for service(service.yaml) that can be create a service to access the application. <br />
command to create the service : kubectl apply -f service.yaml

Click on the below button to import the collection of endpoints to postman.<br/>
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/ee70573e05bd7e0c3b02) <br />
<br/>
[Note: the ip address of all the requests must be changed according to the server the application is deployed to and also the file people_info.csv has to download to local directory to use it in the upload request.]

Summary of the approach used: <br/>

We maintain a seperate OperationStatus table to keep track of user's operations on any file. We also provide rest api through which the user can change the state of the operations(ie., to either stop, terminate or resume the process). The operation requested by the user is executed in a batched manner where for each batch we check the state of the operations. If the user has requested to say terminate an operation, using our endpoint which updates the OperationStatus table . We then read this state change and take action accordingly(in this case we stop the execution and return from the server code).