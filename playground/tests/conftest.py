import pytest_container

TW = pytest_container.Container(url="containers-storage:localhost/playground",forwarded_ports=[pytest_container.PortForwarding(container_port=8001)])
CONTAINER_IMAGES = [TW]

def pytest_generate_tests(metafunc):
    pytest_container.auto_container_parametrize(metafunc)