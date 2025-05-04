WSL account: anhtupham99/B@dmeetsevil1999xx

Apparently in order to work with the Web UI of Airflow I have to connect to either the webserver or scheduler container through:
- Run "sudo docker ps" to get the container ID
- Run "sudo docker exec -it <container_id> bash to connect to a specific container
- Use this account: airflow/badmeetsevil9x (3 eee I don't know why)
- Run "sudo docker-compose up -d" to run the wev UI
- Run "sudo docker-compose down (add -v if want to remove volumns and network, new container will be created next time - not recommended)" to shut down the server and remove all the containers
- Run "source <env>/bin/activate to activate the environment (/ for WSL, \ for cmd or PowerShell)

Operation commands:
- airflow users list: check users
- Create user: airflow users create --username <username> --firstname <name> --lastname <name> --role Admin --email <mail>

NOTE: You can only run airflow in an interpreter that created airflow.