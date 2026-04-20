# cpustate

Persist CPU power settings across boot and sleep on Linux. Applies governor, EPP, and optionally ryzenadj TDP limits via a simple config file and systemd integration.

## Features

- Sets CPU governor and EPP on boot and resume from sleep
- Optional ryzenadj support for AMD Ryzen laptops
- Named profiles (`battery`, `gaming`, etc.)
- Auto-detects CPU capabilities — safe to install on any Linux machine
- Zero runtime dependencies (stdlib only)

## Installation

### From AUR

```bash
yay -S cpustate
```
_Note that your AUR helper might be other than yay._
### Manual

```bash
git clone https://github.com/yourusername/cpustate
cd cpustate
pip install --user .
```

## Setup

Enable the systemd service so settings apply on boot:

```bash
sudo systemctl enable --now cpustate
```

The sleep hook is installed automatically and re-applies settings after resume.

## Config

Edit your config:

```bash
cpustate edit
```

Config is loaded from `~/.config/cpustate.conf` (user) or `/etc/cpustate.conf` (system).

```toml
[cpu]
governor = "performance"
epp = "balance_performance"

[ryzenadj]
stapm-limit = 25000
fast-limit = 28000
slow-limit = 25000
tctl-temp = 95

[profiles.battery]
[profiles.battery.cpu]
governor = "powersave"
epp = "power"
```

## Commands

```
cpustate apply [--profile <name>]   Apply settings (or a named profile)
cpustate status                      Show current governor, EPP, and freq
cpustate edit                        Open config in $EDITOR
cpustate list-profiles               List profiles defined in config
```

## Requirements

- Python 3.11+
- `ryzenadj` (optional, AUR: `ryzenadj-git`) for TDP control

## License

Project is under the GNU GPLv3 license.

## Contributing

You are welcome to contribute to the code. To do so, e-mail me at itspixelatd@proton.me