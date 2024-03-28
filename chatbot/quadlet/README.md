### Run chatbot-langchain as a systemd service

```bash
cp chatbot.yaml /etc/containers/systemd/chatbot.yaml
cp chatbot.kube.example /etc/containers/chatbot.kube
cp chatbot.image /etc/containers/chatbot.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start chatbot
```
