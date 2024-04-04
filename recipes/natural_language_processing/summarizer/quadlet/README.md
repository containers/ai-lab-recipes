### Run summarizer as a systemd service

```bash
cp ../build/summarizer.yaml /etc/containers/systemd/summarizer.yaml
cp ../build/summarizer.kube /etc/containers/summarizer.kube
cp ../build/summarizer.image /etc/containers/summarizer.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start summarizer
```
