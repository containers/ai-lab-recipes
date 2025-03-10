### Run chatbot as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/function-callling-nodejs.yaml ../build/function-callling-nodejs.kube ../build/function-callling-nodejs.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start function-callling-nodejs
```
