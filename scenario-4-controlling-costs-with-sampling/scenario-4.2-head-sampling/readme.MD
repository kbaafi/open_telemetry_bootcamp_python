# Scenario 4.2 Implementing a simple  Headbased Sampling in the Collector

In this scenario we build a [custom headbased sampler](./src/custom_sampler.py) that makes a decision to sample based on data in the span attributes. The custom sampler is shown below:

```python
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
```

The sampler is then chosen when creating the tracing provider as shown below:

```python
# define traces
tracer_provider = TracerProvider(
        resource=resource, sampler=CustomHeadBasedSampler()
)
```

The attributes can be set when creating the span, and this will determine whether a trace will be sampled or not.
