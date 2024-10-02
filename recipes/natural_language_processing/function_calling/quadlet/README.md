### Run function calling as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/function_calling.yaml ../build/function_calling.kube ../build/function_calling.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start function_calling
```
