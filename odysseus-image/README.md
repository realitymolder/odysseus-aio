# Odysseus Docker Image

Automated Docker image builds for [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) AI workspace.

## Image

```
docker.io/realitymolder/odysseus
```

## Tags

| Tag | Branch | Description |
|---|---|---|
| `stable` | `main` | Latest stable release |
| `YYYY-MM-DD` | `main` | Date-stamped stable release |
| `dev` | `dev` | Latest development build |
| `dev-YYYY-MM-DD` | `dev` | Date-stamped dev build |

## Usage

```bash
# Stable (production)
docker pull realitymolder/odysseus:stable

# Development (latest features)
docker pull realitymolder/odysseus:dev

# Specific date
docker pull realitymolder/odysseus:2026-06-20
```

## Build

Images are built automatically via GitHub Actions:

- **Push to `main`** → tagged as `stable` + date
- **Daily schedule (06:00 UTC)** → tagged as `dev` + date
- **Manual dispatch** → configurable branch and tag

## Setup

### GitHub Secrets

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |

### Creating a Docker Hub token

1. Go to [hub.docker.com/settings/security](https://hub.docker.com/settings/security)
2. Create a new access token (Read & Write)
3. Add it as `DOCKERHUB_TOKEN` in your GitHub repo settings → Secrets → Actions

## Links

- [Odysseus upstream](https://github.com/pewdiepie-archdaemon/odysseus)
- [Docker Hub](https://hub.docker.com/r/realitymolder/odysseus)
- [CA Templates](https://github.com/realitymolder/odysseus-ca-templates)
