from opentelemetry import metrics, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler
from prometheus_client import start_http_server


def init_tracer(service_name: str, metrics_port: int, traces_endpoint: str):
    resource = Resource(attributes={SERVICE_NAME: service_name})

    # define metrics
    start_http_server(metrics_port)

    metrics_provider = MeterProvider(
        resource=resource, metric_readers=[PrometheusMetricReader()]
    )
    metrics.set_meter_provider(metrics_provider)

    # define traces
    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(
        SimpleSpanProcessor(
            JaegerExporter(collector_endpoint=traces_endpoint),
        )
    )
    trace.set_tracer_provider(tracer_provider=tracer_provider)

    return metrics.get_meter(service_name), trace.get_tracer(service_name)
