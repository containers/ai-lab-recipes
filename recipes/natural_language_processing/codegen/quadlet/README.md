### Run code-generation as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/codegen.yaml ../build/codegen.kube /usr/share/containers/systemd/codegen.kube ../build/codegen.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start codegen
```
