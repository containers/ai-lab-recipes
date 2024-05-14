import pytest_container
import os

REGISTRY = os.getenv("REGISTRY", "ghcr.io")
IMAGE_NAME = os.getenv("IMAGE_NAME", "containers/object_detection_python:latest")
MODEL_NAME = os.getenv("MODEL_NAME", "facebook/detr-resnet-101")
MODELS_DIR = os.getenv("MODELS_DIR", "/app/models")

MODEL_PATH = f"{MODELS_DIR}/{MODEL_NAME}"

PORT = os.getenv("PORT", 8000)
if type(PORT) == str:
    try:
        PORT = int(PORT)
    except:
        PORT = 8000

MS = pytest_container.Container(
        url=f"containers-storage:{REGISTRY}/{IMAGE_NAME}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path=f"{MODEL_PATH}",
                host_path=f"./{MODEL_NAME}",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": f"{MODEL_PATH}",
            "HOST": "0.0.0.0",
            "PORT": f"{PORT}",
            "IMAGE_NAME": f"{IMAGE_NAME}",
            "REGISTRY": f"{REGISTRY}"
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
