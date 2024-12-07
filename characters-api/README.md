### FastAPI and Traefik with Monitoring by Prometheus and Grafana

##### This project demonstrates a robust setup using FastAPI, Traefik for routing and reverse proxy, Prometheus for metrics collection, and Grafana for visualization.

#####  **1. Getting Started**

Prerequisites:
• Docker
• Docker Compose

##### **Steps to Launch**
1. Clone the Repository
2. Build and Start the Containers:


    uvicorn main:app --reload
or

    docker-compose up --build

### Services:
   * FastAPI: http://localhost:8000
   * Traefik Dashboard: http://localhost:8080
   * Prometheus: http://localhost:9090
   * Grafana: http://localhost:3001 (Use admin as the password)

##### Traefik
Traefik handles HTTP routing and exposes metrics for Prometheus on port 8899.
##### FastAPI
A FastAPI application providing a RESTful API for managing character data (creation, retrieval, update, deletion).
##### Prometheus
Collects metrics from Traefik (target: localhost:8899).
##### Grafana
Visualizes metrics provided by Prometheus.  Import the pre-configured dashboard using ID 4475.

## Working with the API

#### Usage:

**Get All Characters**
```
curl -X GET "http://localhost:8000/characters"
```

**Create a New Character**
```
curl -X POST "http://localhost:8000/character" \
-H "Content-Type: application/json" \
-d '{ "name": "New Character", "universe": "Marvel", "weight": 70.5 }'
```

**Get Character by Name**
```
curl -X GET "http://localhost:8000/character?name=New%20Character"
```

**Update a Character**
```
curl -X PUT "http://localhost:8000/character" \
-H "Content-Type: application/json" \
-d '{ "name": "Existing Character", "universe": "DC", "weight": 75.0 }'
```

**Delete a Character**
```
curl -X DELETE "http://localhost:8000/character?name=New%20Character"
```

**Test Database Connection**
```
curl -X GET "http://localhost:8000/test-db"
```



**▎Grafana Dashboard Setup**
1. Log in to Grafana using admin/admin.
2. Navigate to "Dashboards" -> "Import".
3. Enter ID 4475 and follow the import instructions.


**▎Logs and Debugging**
FastAPI's built-in logging system directs logs to the container's standard output.

