# Intro to the Otel Collector Gateway

In this scenario, we remove the direct connection of the microservices to the signals backends (Prometheus and Jaeger), replacing them with a connection to the OpenTelemetry Collector Gateway which will be configured to provide traces to Jaeger and 'scrapable' metrics to Prometheus

## 1. Modifications to Docker Compose:
The Open Telemtry Collector gateway service is added to Docker Compose.
```yaml
services:
  collector_gateway:
    image: otel/opentelemetry-collector-contrib
    volumes: 
      - ./config/collector-gateway.yml:/etc/otel-collector-config.yaml
    command: ["--config=/etc/otel-collector-config.yaml"]
    ports:
      - "1888:1888"   # pprof extension
      - "8888:8888"   # Prometheus metrics exposed by the collector
      - "8889:8889"   # Prometheus exporter metrics
      - "13133:13133" # health_check extension
      - "4318:4318"   # OTLP HTTP receiver
      - "55670:55679" # zpages extension
```

The collector gateway is configured to receive signals from 


## 2. Redirect Signals to Otel Collector Gateway:
In this variation of the Otel Collector's deployment, the Microservices are instrumented to talk directly to the Collector Gateway.

