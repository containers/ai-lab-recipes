### Run rag as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/rag.yaml ../build/rag.kube ../build/rag.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start rag
```
