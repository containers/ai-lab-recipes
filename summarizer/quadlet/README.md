### Run summarizer as a systemd service

```bash
cp summarizer.yaml /usr/share/containers/systemd/summarizer.yaml
cp summarizer.kube.example /usr/share/containers/summarizer.kube
cp summarizer.image /usr/share/containers/summarizer.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start summarizer
```
