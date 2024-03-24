import pytest_container


def test_alive(auto_container: pytest_container.container.ContainerData, host):
    res = host.run_expect([0],f"curl localhost:{auto_container.forwarded_ports[0].host_port}",).stdout.strip()