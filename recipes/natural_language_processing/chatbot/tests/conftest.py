import pytest_container
import os
import pytest
from selenium import webdriver


MS = pytest_container.Container(
        url=f"containers-storage:{os.environ['REGISTRY']}/model_servers",
        volume_mounts=[
            pytest_container.container.BindMount(
                container_path="/locallm/models",
                host_path="./",
                flags=["ro"]
            )
        ],
        extra_environment_variables={
            "MODEL_PATH": "models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
            "HOST": "0.0.0.0",
            "PORT": "8001"
        },
        forwarded_ports=[
            pytest_container.PortForwarding(
                container_port=8001,
                host_port=8001
            )
        ],
        extra_launch_args=["--net=host"]
    )

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

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument("--headless")
    return chrome_options

@pytest.fixture
def custom_selenium(selenium, firefox_options):
    selenium.webdriver = webdriver.Firefox(firefox_options=firefox_options)
    yield selenium
    selenium.webdriver.quit()
