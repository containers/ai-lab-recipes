# Bootc image with Kepler and OpenTelemetry Collector

Follow this to build a bootc image with a chatbot, kepler, and opentelemetry-collector systemd services.
This example assumes mTLS authentication. The Containerfile assumes certificate and keys
are in `./mTLS` directory. Adjust the Containerfile accordingly. For an example setting up mTLS to send OTLP data to
an OpenTelemetry Collector running in OpenShift, see
[redhat-et/edge-ocp-observability](https://github.com/redhat-et/edge-ocp-observability/blob/main/observability-hub/mtls/generate_certs.sh).
[kepler/otelcol-config.yaml](./kepler/otelcol-config.yaml) is an example collector configuration. Replace the OTLP_EXPORT_ENDPOINT with a real value and
uncomment the otlphttp exporter in the metrics pipeline to export the data if sending to an external endpoint.
As is, OTLP metrics from Kepler will be visible in opentelemetry-collector logs with `systemctl status opentelemetry-collector`.

Before running the below, update the Containerfile or populate a `mTLS` directory with expected files.
Also, update the opentelemetry collector configuration file to match your needs.

```bash
cd recipes/natural_language_processing/chatbot
make BOOTC_IMAGE=quay.io/sallyom/centos-bootc:chatbot ARCH=x86_64 CONTAINERFILE=bootc/Containerfile.nocache bootc

cd ../../../observability
podman build \
    --from quay.io/sallyom/centos-bootc:chatbot \
    --arch x86_64 \
    --security-opt label=disable \
    --cap-add SYS_ADMIN \
    -t quay.io/sallyom/centos-bootc:chatbot-kepler .
```
