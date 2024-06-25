import os
import time
from datetime import datetime
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

service_name = os.getenv("WORKFLOW_NAME", "default_service")
job_name = os.getenv("JOB_NAME", "default_job")

resource = Resource.create({"service.name": service_name})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)
console_span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(console_span_processor)

# Adding OTLP Span Exporter for actual data export
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)
otlp_span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(otlp_span_processor)

print("Tracer initialized with service name:", service_name)

def set_start_time():
    start_time = datetime.now().timestamp()
    with open("/tmp/start_time.txt", "w") as file:
        file.write(str(start_time))
    print("Start time recorded")

def calculate_duration():
    with open("/tmp/start_time.txt", "r") as file:
        start_time = float(file.read())
    end_time = datetime.now().timestamp()
    duration = end_time - start_time
    print(f"Total Duration: {duration}s")
    with tracer.start_as_current_span(job_name) as span:
        span.set_attribute("total_duration_s", duration)

if __name__ == "__main__":
    action = os.getenv("TRACE_ACTION", "start")

    if action == "start":
        set_start_time()
    elif action == "end":
        calculate_duration()
