### Run chatbot as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/chatbot.yaml ../build/chatbot.kube ../build/chatbot.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start chatbot
```
