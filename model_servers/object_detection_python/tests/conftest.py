import pytest_container
import pytest
import os
import logging
import platform

if 'PORT' not in os.environ:
    PORT = 8000
else:
    PORT = os.environ['PORT']
    try:
        PORT = int(PORT)
    except:
        PORT = 8000

if 'IMAGE' not in os.environ:
    IMAGE = 'ghcr.io/containers/model_servers/object_detection_python:latest'
else:
    IMAGE = os.environ['IMAGE']

MODEL_NAME=os.environ['MODEL_NAME']
MODEL_PATH=os.environ['MODEL_PATH']

BIND_MOUNT_OPTIONS = 'ro'

MS = pytest_container.Container(
        url=f"containers-storage:{IMAGE}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path=f"{MODEL_PATH}",
                host_path=f"./{MODEL_NAME}",
                flags=[BIND_MOUNT_OPTIONS]
            )
        ],
        extra_environment_variables={
            "MODEL_NAME": f"{MODEL_NAME}",
            "MODEL_PATH": f"{MODEL_PATH}",
            "HOST": "0.0.0.0",
            "PORT": f"{PORT}"
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port=PORT,
                host_port=PORT
            )
        ],
    )

def pytest_addoption(parser):
    pytest_container.add_logging_level_options(parser)


def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)
