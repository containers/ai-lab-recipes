import pytest_container
import os

if not 'REGISTRY' in os.environ:
    REGISTRY = 'ghcr.io'
else:
    REGISTRY = os.environ['REGISTRY']

if not 'IMAGE_NAME' in os.environ:
    IMAGE_NAME = 'containers/whispercpp:latest'
else:
    IMAGE_NAME = os.environ['IMAGE_NAME']

if not 'MODEL_NAME' in os.environ:
    MODEL_NAME = 'ggml-small.bin'
else: 
    MODEL_NAME = os.environ['MODEL_NAME']

if not 'MODEL_PATH' in os.environ:
    MODEL_PATH = "/app/models"
else:
    MODEL_PATH = os.environ['MODEL_PATH']

if not 'PORT' in os.environ:
    PORT = 8001
else:
    PORT = os.environ['PORT']
    try:
        PORT = int(PORT)
    except:
        PORT = 8001

MS = pytest_container.Container(
        url=f"containers-storage:{REGISTRY}/{IMAGE_NAME}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path="{MODEL_PATH}/{MODEL_NAME}".format(MODEL_PATH=MODEL_PATH, MODEL_NAME=MODEL_NAME),
                host_path=f"./{MODEL_NAME}",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": "{MODEL_PATH}/{MODEL_NAME}".format(MODEL_PATH=MODEL_PATH, MODEL_NAME=MODEL_NAME),
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

def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)

def pytest_addoption(parser):
    pytest_container.add_logging_level_options(parser)
