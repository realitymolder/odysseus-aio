# **This repo is being split into 3 dedicated repositories. Hold tight — a more robust structure is coming.**

# Odysseus Unraid

[Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) is a self-hosted AI workspace — chat, agents, deep research, documents, email, calendar, and model Cookbook. This repository provides Docker images and a Compose stack to run Odysseus on your Unraid server.

## Prerequisites

An automated GitHub Action builds and publishes the Docker image to GitHub Container Registry.

### Setup for first-time use

1. **Fork or push this repo** to your own GitHub account
2. **Enable GitHub Actions**: Settings → Actions → General → Allow all actions
3. **Enable package creation**: Settings → Actions → General → Workflow permissions → "Read and write permissions" + "Allow GitHub Actions to create and approve pull requests"
4. **Push to `main`** — the workflow in `.github/workflows/docker-publish.yml` builds and pushes the image to `ghcr.io/realitymolder/odysseus-unraid:latest`
5. **Make the package public**: repo → Packages → select the package → Package settings → Change visibility to public

## Option A: AIO One-Click Install (Recommended)

Single container that auto-deploys and manages the full stack.

| Container | Image | Host Port |
|---|---|---|
| `odysseus-aio-app` | `ghcr.io/realitymolder/odysseus-unraid:latest` | 7000 |
| `odysseus-aio-chromadb` | `chromadb/chroma:latest` | 8100 |
| `odysseus-aio-searxng` | `searxng/searxng:latest` | 8080 |
| `odysseus-aio-ntfy` | `binwiederhier/ntfy` | 8091 |

### Install steps

1. Deploy via `docker compose -f docker-compose.aio.yml up -d` or install the AIO image through Unraid
2. Access the management UI at `http://<your-unraid-ip>:9000`
3. Use the management UI to deploy, stop, update, or monitor containers

> **Note:** The AIO container requires Docker socket access (`/var/run/docker.sock`) to manage sibling containers.

## Option B: Docker Compose

For non-Unraid setups or manual control.

```bash
docker compose up -d
```

This deploys all 4 containers (Odysseus, ChromaDB, SearXNG, ntfy) as a single stack. Edit environment variables in the compose file or create a `.env` file to configure LLM providers, ports, and paths.

See `docker-compose.yml` for the full stack or `docker-compose.aio.yml` for the AIO master container. See [docs/docker-compose.md](docs/docker-compose.md) for maintenance notes.

## Post-install

1. Open the Odysseus WebUI:
   - **AIO:** Management UI at `http://<your-unraid-ip>:9000`, app at port 7000
   - **Docker Compose:** `http://<your-unraid-ip>:7000`
2. Find the auto-generated admin password in container logs: **Docker** → select container → **Logs**
3. Log in with username `admin` (or the value of `ODYSSEUS_ADMIN_USER`)
4. Change the password in **Settings**
5. Configure your LLM provider in **Settings** — add Ollama, OpenAI, or a local endpoint

## GPU passthrough (optional)

For NVIDIA GPUs, install the **NVIDIA Container Toolkit** on your Unraid host via the Nvidia Drivers plugin, then add these extra parameters to the Odysseus container:

```
--runtime=nvidia
-e NVIDIA_VISIBLE_DEVICES=all
```

## Updating

- **AIO:** Use the management UI at port 9000 (Update All button), or update the AIO image through Unraid and it will pull latest companion images on next deploy.
- **Docker Compose:** `docker compose pull && docker compose up -d`

## License

Odysseus: [MIT](https://github.com/pewdiepie-archdaemon/odysseus/blob/dev/LICENSE)
