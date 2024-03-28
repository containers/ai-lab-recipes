### Run chatbot as a systemd service

```bash
cp chatbot.yaml /usr/share/containers/systemd/chatbot.yaml
cp chatbot.kube.example /usr/share/containers/chatbot.kube
cp chatbot.image /usr/share/containers/chatbot.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start chatbot
```
