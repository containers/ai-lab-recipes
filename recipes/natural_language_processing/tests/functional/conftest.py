import pytest_container
import os
import logging

IMAGE_NAME=os.environ['IMAGE_NAME'] # REQUIRED
MODEL_NAME=os.environ['MODEL_NAME'] # REQUIRED

if not 'REGISTRY' in os.environ:
    REGISTRY = 'quay.io'
else:
    REGISTRY=os.environ['REGISTRY']

if not 'MODEL_SERVER_PORT' in os.environ:
    MODEL_SERVER_PORT=8001
else
    MODEL_SERVER_PORT=os.environ['MODEL_SERVER_PORT']
    try:
        MODEL_SERVER_PORT = int(MODEL_SERVER_PORT)
    except:
        MODEL_SERVER_PORT = 8001

if not 'MODEL_PATH' in os.environ:
    MODEL_PATH='/app/models'
else
    MODEL_PATH=os.environ['MODEL_PATH']

if not 'MODEL_ENDPOINT' in os.environ:
    MODEL_ENDPOINT='10.88.0.1'
else
    MODEL_ENDPOINT=os.environ['MODEL_ENDPOINT']

if not 'MODEL_SERVER_PORT' in os.environ:
    MODEL_SERVER_PORT = 8001
else
    MODEL_SERVER_PORT = os.environ['MODEL_SERVER_PORT']

logging.info("""
Starting pytest with the following ENV vars:
    REGISTRY:                   {REGISTRY}
    IMAGE_NAME:                 {IMAGE_NAME}
    MODEL_PATH:                 {MODEL_PATH}
    MODEL_NAME:                 {MODEL_NAME}
    MODEL_SERVER_PORT:          {MODEL_SERVER_PORT}
    MODEL_ENDPOINT:             {MODEL_ENDPOINT}
For:
    model_server: whispercpp
""".format(REGISTRY=REGISTRY, IMAGE_NAME=IMAGE_NAME, MODEL_NAME=MODEL_NAME, MODEL_PATH=MODEL_PATH, MODEL_SERVER_PORT=MODEL_SERVER_PORT, MODEL_ENDPOINT=MODEL_ENDPOINT))

MS = pytest_container.Container(
        url=f"containers-storage:{REGISTRY}/{IMAGE_NAME}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path=f"{MODEL_PATH}/${MODEL_NAME}",
                host_path=f"./{MODEL_NAME}",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": f"{MODEL_PATH}/{MODEL_NAME}",
            "HOST": "{MODEL_ENDPOINT}",
            "MODEL_SERVER_PORT": "{MODEL_SERVER_PORT}"
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port={MODEL_SERVER_PORT},
                host_port={MODEL_SERVER_PORT}
            )
        ],
    )

CB = pytest_container.Container(
        url=f"containers-storage:{os.environ['REGISTRY']}/containers/{os.environ['IMAGE_NAME']}",
        extra_environment_variables={
            "MODEL_ENDPOINT": MODEL_ENDPOINT
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port=8501,
                host_port=8501
            )
        ],
    )

def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)

def pytest_addoption(parser):
    pytest_container.add_logging_level_options(parser)
