### Run audio-to-text as a systemd service

There are pre-built images and a pod definition to run this audio-to-text example application.
This sample converts an audio waveform (.wav) file to text.

To run locally, 

```bash
podman kube play ./build/audio-to-text.yaml
```
To monitor locally,

```bash
podman pod list
podman ps 
podman logs <name of container from the above>
```

The application should be accessible at `http://localhost:8501`. It will take a few minutes for the model to load.

### Run audio-to-text as a systemd service

```bash
(cd ../;make quadlet)
sudo cp ../build/audio-to-text.yaml ../build/audio-to-text.kube ../build/audio-to-text.image /usr/share/containers/systemd/
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start audio-to-text
```
