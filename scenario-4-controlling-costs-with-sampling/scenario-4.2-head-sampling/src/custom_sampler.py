from opentelemetry.sdk.trace.export import BatchSpanProcessor, SimpleSpanProcessor
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision


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
