# Odysseus Unraid Community App

[Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) is a self-hosted AI workspace — chat, agents, deep research, documents, email, calendar, and model Cookbook. This repository provides the Unraid Community Applications (CA) templates to run Odysseus on your Unraid server.

**Two deployment paths:**

| | Standalone (CA Templates) | AIO (All-In-One) |
|---|---|---|
| **What installs** | Odysseus + ChromaDB (SearXNG & ntfy via CA deps) | Single container auto-deploys everything |
| **Management** | Unraid Docker page | Built-in web UI on port 9000 |
| **Best for** | Custom configs, selective companions | One-click setup, minimal maintenance |

## Repository Structure

This repo contains everything needed for both deployment methods:

| Directory | Purpose | Future Repo |
|---|---|---|
| `ca-templates/` | CA template XML files, icons, CI validation | `odysseus-ca-templates` |
| `odysseus-image/` | Main Odysseus Docker image build (pushes to Docker Hub) | `odysseus` |
| `aio/` | AIO master container (Dockerfile, orchestrator, web UI) | stays here as `odysseus-aio` |
| `templates/` | CA templates for Unraid (references Docker Hub images) | stays here |

## Prerequisites

Images are published to **Docker Hub** at `realitymolder/odysseus` and `realitymolder/odysseus-aio`.

### Docker Hub setup (one-time)

1. Create a Docker Hub access token at [hub.docker.com/settings/security](https://hub.docker.com/settings/security)
2. In each GitHub repo (`odysseus`, `odysseus-aio`), add secrets:
   - `DOCKERHUB_USERNAME` = `realitymolder`
   - `DOCKERHUB_TOKEN` = your access token

## Option A: Standalone Install (CA Templates)

Individual templates with CA dependency resolution.

### Templates

| Template | Image | Description |
|---|---|---|
| `templates/odysseus.xml` | `realitymolder/odysseus:latest` | Main AI workspace |
| `templates/chromadb.xml` | `chromadb/chroma:latest` | Vector store for semantic memory |

SearXNG and ntfy are pulled in automatically via CA dependency declarations.

### Install steps

1. Add this repo to CA: **Apps** → **Settings** → **Template Repositories** → Add `https://github.com/realitymolder/Odysseus-Unraid`
2. Install **Odysseus** — CA prompts for ChromaDB, SearXNG, and ntfy automatically
3. Confirm all containers are named correctly (defaults are preconfigured):
   - `odysseus-chromadb`
   - `odysseus-searxng`
   - `odysseus-ntfy`

The main Odysseus container connects to companions via these Docker internal hostnames.

## Option B: AIO One-Click Install (Recommended)

Single container that auto-deploys and manages the full stack.

### Templates

| Template | Image | Description |
|---|---|---|
| `templates/odysseus-aio.xml` | `realitymolder/odysseus-aio:latest` | Master container — deploys everything |

On first start, AIO automatically provisions:

| Container | Image | Host Port |
|---|---|---|
| `odysseus-aio-app` | `realitymolder/odysseus:stable` | 7000 |
| `odysseus-aio-chromadb` | `chromadb/chroma:latest` | 8100 |
| `odysseus-aio-searxng` | `searxng/searxng:latest` | 8080 |
| `odysseus-aio-ntfy` | `binwiederhier/ntfy` | 8091 |

The AIO pulls the upstream Odysseus image based on the `ODYSSEUS_APP_IMAGE` env var (default: `realitymolder/odysseus:stable`). Set to `realitymolder/odysseus:dev` for development builds.

### Install steps

1. Add this repo to CA (same as above)
2. Install **Odysseus-AIO**
3. Access the management UI at `http://<your-unraid-ip>:9000`
4. Use the management UI to deploy, stop, update, or monitor containers

> **Note:** The AIO container requires Docker socket access (`/var/run/docker.sock`) to manage sibling containers.

## Option C: Docker Compose (Advanced)

For non-Unraid setups or manual control.

```bash
docker compose up -d
```

This deploys all 4 containers (Odysseus, ChromaDB, SearXNG, ntfy) as a single stack. Edit environment variables in the compose file or create a `.env` file to configure LLM providers, ports, and paths.

See `docker-compose.yml` for the full stack or `docker-compose.aio.yml` for the AIO master container.

## Image Tags

| Tag | Branch | Description |
|---|---|---|
| `stable` | `main` | Latest stable release |
| `YYYY-MM-DD` | `main` | Date-stamped stable release |
| `dev` | `dev` | Latest development build |
| `dev-YYYY-MM-DD` | `dev` | Date-stamped dev build |

```bash
# Pull specific versions
docker pull realitymolder/odysseus:stable
docker pull realitymolder/odysseus:dev
docker pull realitymolder/odysseus:2026-06-20
```

## Post-install

1. Open the Odysseus WebUI:
   - **Standalone:** `http://<your-unraid-ip>:7000`
   - **AIO:** Management UI at `http://<your-unraid-ip>:9000`, app at port 7000
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

- **Standalone:** Pull the latest image, then **Docker** → force update the container. Update companions individually through the Unraid Docker page.
- **AIO:** Use the management UI at port 9000 (Update All button), or update the AIO image through Unraid and it will pull latest companion images on next deploy.
- **Docker Compose:** `docker compose pull && docker compose up -d`

## License

Templates: [MIT](LICENSE)
Odysseus: [MIT](https://github.com/pewdiepie-archdaemon/odysseus/blob/dev/LICENSE)
