import pytest_container
import os
import logging

REGISTRY=os.environ['REGISTRY']
IMAGE_NAME=os.environ['IMAGE_NAME']
MODEL_NAME=os.environ['MODEL_NAME']

logging.info("""
Starting pytest with the following ENV vars:
    REGISTRY: {REGISTRY}
    IMAGE_NAME: {IMAGE_NAME}
    MODEL_NAME: {MODEL_NAME}
For:
    model_server: whispercpp
""".format(REGISTRY=REGISTRY, IMAGE_NAME=IMAGE_NAME, MODEL_NAME=MODEL_NAME))


MS = pytest_container.Container(
        url=f"containers-storage:{REGISTRY}/{IMAGE_NAME}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path=f"/locallm/models/${MODEL_NAME}",
                host_path=f"./{MODEL_NAME}",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": f"/locall/models/{MODEL_NAME}",
            "HOST": "0.0.0.0",
            "PORT": "8001"
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port=8001,
                host_port=8001
            )
        ],
    )

CB = pytest_container.Container(
        url=f"containers-storage:{os.environ['REGISTRY']}/containers/{os.environ['IMAGE_NAME']}",
        extra_environment_variables={
            "MODEL_ENDPOINT": "http://10.88.0.1:8001"
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
