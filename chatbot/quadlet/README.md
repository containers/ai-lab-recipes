### Run chatbot as a systemd service

```bash
cp chat.yaml /etc/containers/systemd/.
cp chatbot.kube.example /etc/containers/chatbot.kube
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start chatbot
``` 
