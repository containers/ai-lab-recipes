### Run summarizer-langchain as a systemd service

```bash
cp summarizer.yaml /etc/containers/systemd/summarizer.yaml
cp summarizer.kube.example /etc/containers/summarizer.kube
cp summarizer.image /etc/containers/summarizer.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start summarizer
```
