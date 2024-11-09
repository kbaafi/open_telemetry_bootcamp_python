# Controlling Costs of Storing and Transmitting Signals using Sampling Strategies

* [A very detailed discussion on the issue of sampling use cases can be found here: ](https://www.youtube.com/watch?v=tb6VHrihPZI&t=2062s)
* [OpenTelemetry's Documentation on Sampling](https://opentelemetry.io/docs/concepts/sampling/)
* [Open Telemetry Blog post on Tail Based Sampling](https://opentelemetry.io/blog/2022/tail-sampling/)

## How much traces to collect
Since sampling introduces loss of signal data we may need to define usecases for when to sample data
1. "I want to debug any request" - requires 100% traffic
1. "I want to debug system wide issues" - 20-50%
1. "I want to know application baseline" - 5-10%
1. "I want to understand system archicture" - 5%

## When to sample
**Head Sampling**: Decision to sample is made when a span start in the SDK
**Tail Sampling**: Collect the entire trace and make a decision to sample when the trace completes. This is done within the Collector

## Tail Sampling
Tail Sampling collects an entire trace before a sampling decision is made in the Collector. Sampling this way means that the Collector is accumulating data in memory before a decision is made. 


1. Define how much data to collect after a parent span has been received before a decision is made using:

    * **decision_wait** setting (default=30s)
    * **num_traces** setting (default=50000)

1.  Take a sampling decision based on

    * always_sample
    * latency (between a min and max)
    * numeric_attribute
    * probabilistic (sample)
    * staus_code
    * string_attribute
    * rate_limiting

## Head Sampling
Within the SDK a sampling decision is made for a span at the start of the span. 

So what happens with downstream services? 

    Downstream services will receive the earlier decision made on the span (whether to sample or not) and the downstream services can make a decision to respect the parent's decision or not.


## Common Use Cases
* Only errors - tail
* Above latency - tail
* Only specific routes/events -head



