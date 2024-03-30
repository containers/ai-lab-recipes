### Run rag as a systemd service

```bash
sudo cp rag.yaml /usr/share/containers/systemd/rag.yaml
sudo cp rag.kube /usr/share/containers/rag.kube
sudo cp rag.image /usr/share/containers/rag.image
sudo /usr/libexec/podman/quadlet --dryrun (optional)
sudo systemctl daemon-reload
sudo systemctl start rag
```
