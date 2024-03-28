### Run audio-text locally as a podman pod

There are pre-built images and a pod definition to run this audio-to-text example application.
This sample converts an audio waveform (.wav) file to text.

To run locally, 

```bash
podman kube play ./quadlet/audio-to-text.yaml
```
To monitor locally,

```bash
podman pod list
podman ps 
podman logs <name of container from the above>
```

The application should be acessible at `http://localhost:8501`. It will take a few minutes for the model to load. 

### Run audio-text as a systemd service

```bash
cp audio-text.yaml /etc/containers/systemd/audio-text.yaml
cp audio-text.kube.example /etc/containers/audio-text.kube
cp audio-text.image /etc/containers/audio-text.image
/usr/libexec/podman/quadlet --dryrun (optional)
systemctl daemon-reload
systemctl start audio-text
```
