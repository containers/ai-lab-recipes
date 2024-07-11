import os
import time
from datetime import datetime
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Initialize MeterProvider and Exporter
service_name = os.getenv("WORKFLOW_NAME", "default_service")
exporter = OTLPMetricExporter(endpoint="localhost:4317", insecure=True)
metric_reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

# Create a counter for job duration
job_duration_histogram = meter.create_histogram(
    name="job_duration_seconds",
    description="Duration of the job in seconds",
    unit="s"
)

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

    # Record the duration in the histogram
    job_duration_histogram.record(duration, {"job_name": os.getenv("JOB_NAME", "default_job")})

if __name__ == "__main__":
    action = os.getenv("METRIC_ACTION", "start")

    if action == "start":
        set_start_time()
    elif action == "end":
        calculate_duration()

