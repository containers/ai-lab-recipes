### Run code-generation as a systemd service

```bash
cp codegen.yaml /etc/containers/systemd/codegen.yaml
cp codegen.kube.example /etc/containers/codegen.kube
cp codegen.image /etc/containers/codegen.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start codegen
```
