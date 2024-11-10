from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision
import random

def should_sample():
        return random.choice([True, False])

class CustomHeadBasedSampler(Sampler):
    def should_sample(self, parent_context, trace_id, name, kind = None, attributes = None, links = None, trace_state = None):
        if attributes and name == "user_api_get_user":
            # Get decision to sample from attributes
            should_sample  = attributes.get("should_sample")

            if should_sample == True:
                print("Sampling in Custom Sampler")
                return SamplingResult(decision=Decision.RECORD_AND_SAMPLE)
            elif should_sample == False:
                print("Dropping Sample")
                return SamplingResult(decision=Decision.DROP)
        else:
            return SamplingResult(decision=Decision.RECORD_AND_SAMPLE)
        
    def get_description(self):
        return "CustomHeadBasedSampler"
        


def init_tracer(service_name: str, signals_endpoint: str):
    resource = Resource(attributes={SERVICE_NAME: service_name})

    collector_metrics_endpoint = f"{signals_endpoint}/v1/metrics"
    collect_traces_endpoint = f"{signals_endpoint}/v1/traces"

    # define metrics provider
    otlp_exporter = OTLPMetricExporter(
        endpoint=collector_metrics_endpoint
    )
    reader = PeriodicExportingMetricReader(otlp_exporter, export_interval_millis=5000)
    metrics_provider = MeterProvider(
        resource=resource,
        metric_readers=[reader]
    )
    metrics.set_meter_provider(metrics_provider)

    # define traces
    tracer_provider = TracerProvider(
        resource=resource, sampler=CustomHeadBasedSampler()
    )

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=collect_traces_endpoint),
        )
    )
    trace.set_tracer_provider(tracer_provider=tracer_provider)

    return metrics.get_meter(service_name), trace.get_tracer(service_name)
