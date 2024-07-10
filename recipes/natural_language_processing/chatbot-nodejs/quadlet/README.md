### Run chatbot as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/chatbot-nodejs.yaml ../build/chatbot-nodejs.kube ../build/chatbot-nodejs.image /usr/share/containers/systemd/
sudo /usr/libexec/podman/quadlet --dryrun #optional
sudo systemctl daemon-reload
sudo systemctl start chatbot-nodejs
```
