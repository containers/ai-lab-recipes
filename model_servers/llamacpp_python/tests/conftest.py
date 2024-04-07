import pytest_container
import os

MS = pytest_container.Container(
        url=f"containers-storage:{os.environ['REGISTRY']}/{os.environ['IMAGE_NAME']}",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path="/locallm/models/model.gguf",
                host_path=f"./model.gguf",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": "/locallm/models/model.gguf",
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

def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)

def pytest_addoption(parser):
    pytest_container.add_logging_level_options(parser)
