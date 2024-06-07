import os
import time
import logging
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import SpanContext, TraceFlags, TraceState, NonRecordingSpan

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenTelemetry tracing
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": os.getenv("WORKFLOW_NAME")})
    )
)
tracer = trace.get_tracer(__name__)

# Set up OTLP exporter to send to OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)

# Set up span processor
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Export to console for debugging
console_exporter = ConsoleSpanExporter()
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(console_exporter))

def retry_operation(operation, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return operation()
        except Exception as e:
            logger.error(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                raise

def start_trace(step_name):
    span = tracer.start_span(name=step_name)
    return span

def end_trace(span):
    span.end()

if __name__ == "__main__":
    step_name = os.getenv("STEP_NAME", "default_step")
    action = os.getenv("TRACE_ACTION", "start")

    if action == "start":
        span = retry_operation(lambda: start_trace(step_name))
        with open(f"/tmp/trace_{step_name}.txt", "w") as f:
            f.write(str(span.get_span_context().trace_id))
    elif action == "end":
        trace_id = os.getenv("TRACE_ID")
        if not trace_id:
            with open(f"/tmp/trace_{step_name}.txt", "r") as f:
                trace_id = f.read().strip()
        trace_id = int(trace_id, 16)
        span_context = SpanContext(
            trace_id=trace_id,
            span_id=0,  # Span ID will be generated
            trace_flags=TraceFlags(TraceFlags.SAMPLED),
            trace_state=TraceState(),
            is_remote=True
        )
        with tracer.start_as_current_span(name=step_name, context=trace.set_span_in_context(NonRecordingSpan(span_context))):
            span = retry_operation(lambda: tracer.start_span(name=step_name))
            retry_operation(lambda: end_trace(span))

