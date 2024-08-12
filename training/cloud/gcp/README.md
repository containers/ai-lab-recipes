# Google Cloud Platform modifications for RHEL AI
Trying to mimic as much as possible the [changes on RHEL for GCP](https://github.com/osbuild/images/blob/main/pkg/distro/rhel/rhel9/gce.go)

## Changes

- Extra kernel parameters

```
net.ifnames=0 biosdevname=0 scsi_mod.use_blk_mq=Y console=ttyS0,38400n8d
```

- Timezone: UTC
- Chrony configuration:
    - Change server
- Locale: en_US.UTF-8
- Keymap: us
- X11 layout: us

- sshd config
    - PasswordAuthentication: false
    - ClientAliveInterval: 420
    - PermitRootLogin: No

- Modules
    - blacklist floppy

- GCPGuestAgentConfig
    - SetBotoConfig: false

- Packages
    - langpacks-en
    - acpid
    - rng-tools
    - vim
    - google-compute-engine
    - google-osconfig-agent
    - gce-disk-expand
    - timedatex
    - tuned

- Remove Packages
    - irqbalance
    - microcode_ctl
