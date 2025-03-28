# UFO

- **[UFO-Real](/src/ufo-real/)**: The real deal, the UFO itself.
- **[UFO-Sure](/src/ufo-sure/)**: The dashboard (UI), to ensure and test the UFO.

## Quickstart

### With Docker
```sh
docker compose up
```

### With Python 3.13
```sh
cd src/ufo
uv run main.py
```

Or with arguments:
```sh
cd src
uv run main.py --bus /dev/serial0 --baudrate 115200 --debug
```

Or to run the demo:
```sh
cd src
uv run main.py --demo --debug
```

## Installation

```sh
git clone https://<PAT>@github.com/pren-hs24/ufo.git
cd ufo
```

### With Docker
```sh
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/raspbian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/raspbian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

```sh
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

### With Python 3.13
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```
