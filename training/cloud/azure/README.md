# Azure for RHEL AI
Trying to mimic as much as possible the [changes on RHEL for Azure](https://github.com/osbuild/images/blob/main/pkg/distro/rhel/rhel9/azure.go)

# Summary
- Extra kernel parameters

Even if in the link [Kernel Parameters on RHEL for Azure](https://github.com/osbuild/images/blob/a4ae81dc3eed3e86c359635e3135fc8a07f411dd/pkg/distro/rhel/rhel9/azure.go#L454) we see other changes, when running a RHEL instance in Azure, the extra kernel parameters are others, so we will take those as our reference
```
loglevel=3 console=tty1 console=ttyS0,115200n8 earlyprintk=ttyS0,115200 net.ifnames=0 cloud-init=disabled
```

Note that we also disable cloud-init via kernel parameter

- Timezone: UTC
- Locale: en_US.UTF-8
- Keymap: us
- X11 layout: us

- sshd config
    - ClientAliveInterval: 180

- Packages
    - hyperv-daemons
    - langpacks-en
    - NetworkManager-cloud-setup
    - nvme-cli
    - patch
    - rng-tools
    - uuid
    - WALinuxAgent

- Services
    - nm-cloud-setup.service
    - nm-cloud-setup.timer
    - waagent

- Systemd
    - nm-cloud-setup.service: `Environment=NM_CLOUD_SETUP_AZURE=yes`

- Kernel Modules
    - blacklist amdgpu
    - blacklist intel_cstate
    - blacklist floppy
    - blacklist nouveau
    - blacklist lbm-nouveau
    - blacklist skx_edac

- Cloud Init
    - 10-azure-kvp.cfg
    - 91-azure_datasource.cfg

- PwQuality
    - /etc/security/pwquality.conf

- WaAgentConfig
    - RDFormat false
    - RDEnableSwap false

- udev rules
    - /etc/udev/rules.d/68-azure-sriov-nm-unmanaged.rules
