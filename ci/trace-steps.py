import os
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

# Initialize Tracer
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.get_tracer_provider().add_span_processor(span_processor)

def trace_step(step_name: str):
    """
    Decorated function that traces execution time.
    Args:
        step_name (str): Name of the step to trace.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(step_name) as span:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                span.set_attribute("duration_s", duration)
                print(f"Step: {step_name}, Duration: {duration}s")
                return result
        return wrapper
    return decorator

def trace_job(job_name: str):
    """
    Decorated function that traces execution time.
    Args:
        job_name (str): Name of the job to trace.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with tracer.start_as_current_span(job_name) as span:
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                duration = end_time - start_time
                span.set_attribute("total_duration_s", duration)
                print(f"Job: {job_name}, Total Duration: {duration}s")
                return result
        return wrapper
    return decorator

@trace_step("Example Step")
def example_step():
    time.sleep(5)  # Simulate work
    return "Step Completed: Example Step"

@trace_job("Example Job")
def example_job():
    step_result = example_step()
    return f"Job Completed: Example Job with {step_result}"

if __name__ == "__main__":
    job_name = os.getenv("WORKFLOW_NAME", "Default Job")
    step_name = os.getenv("STEP_NAME", "Default Step")
    trace_action = os.getenv("TRACE_ACTION", "start")

    if trace_action == "start":
        example_job()
    elif trace_action == "end":
        print(f"Ending trace for {job_name} - {step_name}")

