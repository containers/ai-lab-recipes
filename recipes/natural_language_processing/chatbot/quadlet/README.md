### Run chatbot as a systemd service

```bash
sudo cp chatbot.yaml /usr/share/containers/systemd/chatbot.yaml
sudo cp chatbot.kube /usr/share/containers/chatbot.kube
sudo cp chatbot.image /usr/share/containers/chatbot.image
sudo /usr/libexec/podman/quadlet --dryrun (optional)
sudo systemctl daemon-reload
sudo systemctl start chatbot
```
