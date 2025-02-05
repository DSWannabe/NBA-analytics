- Check docker if installed properly: sudo docker run hello-world
- Portainer ID/PW: anhtupham99/B@dmeetsevil9xpip install apache-airflow
- Access Portainer: localhost:9000
- Check docker status: systemctl status docker
- Check if a port is in use: sudo lsof -i: <port_number>
- Check what container is using which port: sudo docker ps
- If you already changed the ports but it's not working, stop then restart:
    + docker-compose down -v -> docker-compose up -d
- If just the airflow webserver alone, run localhost:8080; If airflow + docker, run localhost:8081 and use default account (ID:airflow/PW:airflow)
