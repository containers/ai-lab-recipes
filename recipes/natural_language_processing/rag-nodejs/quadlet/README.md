### Run rag-nodejs as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/rag-nodejs.yaml ../build/rag-nodejs.kube ../build/rag-nodejs.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start rag-nodejs
```
