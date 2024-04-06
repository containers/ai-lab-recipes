### Run summarizer as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/summarizer.yaml ../build/summarizer.kube ../build/summarizer.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start summarizer
```
