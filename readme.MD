# Open Telemetry Bootcamp Python
---
This is my follow-along in Python of the [OpenTelemetry Bootcamp by Michael Haberman](https://www.youtube.com/watch?v=UEwkn0iHDzA&list=PLNxnp_rzlqf6z1cC0IkIwp6yjsBboX945). The original work was done in TypeScript and can be found at [https://github.com/aspecto-io/opentelemetry-bootcamp/](https://github.com/aspecto-io/opentelemetry-bootcamp/)

This work follows the instrumentation of a set of microservices by implementing the following scenarios:
1. Basic and Auto Instrumentation of Web Services
2. Context Propagation (transfer of tracing contexts between different runtimes)
3. Implementation of the OpenCollector Agent and Gateway
4. (Not yet implemented) Sampling Strategies
5. (Not yet implemented) Custom Instrumentation

The scenarios are implemented in Docker Compose for easy verification. 

Each scenario is packaged as its own project and can be run independently. 

## Services Implemented
1. **The Redis cache**
2. **The User service**

    This service is available at port `8000` and exposes a `/user` endpoint i.e `http://localhost:8000/user` which retrieves a random `user` from the list of users provided by the RemoteUsers service

    The service also hosts a web socket on port 8000 at the `/ws` endpoint

3. **The RemoteUsers service**
    
    This service produces a set of fictitious users with the following attributes `[username, firstname, lastname, emailAddress]`. The service is available on the `8001` port and exposes a `/get_users` endpoint

4. **The Items service**

    This service is availabe on the port `8002` and exposes the following endpoints

    * `/ws` for communicating with the User Service's websocket
    * `/data` for retrieving a user from the User Service
    * `/pub` for publishing a message to Redis

5. **The Redis Subscriber**
    
    This daemon subscribes to and responds to messages published to Redis

## Instrumentation Services
1. **Prometheus:** This service is available on port `9090`
2. **Jaeger:** This service is available on port  `16686`