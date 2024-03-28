import pytest_container
import os


CB = pytest_container.Container(
        url=f"containers-storage:{os.environ['REGISTRY']}/{os.environ['IMAGE_NAME']}",
        extra_environment_variables={
            "MODEL_SERVICE_ENDPOINT": "http://10.88.0.1:8001/v1"
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port=8501,
                host_port=8501
            )
        ],
        extra_launch_args=["--net=host"]
    )

def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)

def pytest_addoption(parser):
    pytest_container.add_logging_level_options(parser)
