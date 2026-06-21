# Odysseus AIO

All-in-one master container for [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) self-hosted AI workspace. One install deploys the full stack: Odysseus, ChromaDB, SearXNG, and ntfy.

## What it does

On first start, the AIO container automatically pulls and provisions:

| Container | Image | Port |
|---|---|---|
| `odysseus-aio-app` | `realitymolder/odysseus:stable` | 7000 |
| `odysseus-aio-chromadb` | `chromadb/chroma:latest` | 8100 |
| `odysseus-aio-searxng` | `searxng/searxng:latest` | 8080 |
| `odysseus-aio-ntfy` | `binwiederhier/ntfy` | 8091 |

A built-in management UI at port 9000 handles deploy, stop, update, and status monitoring.

## Image

```
docker.io/realitymolder/odysseus-aio:latest
```

## Quick start

### Unraid (CA template)

1. Add this repo to CA: **Apps** → **Settings** → **Template Repositories** → `https://github.com/realitymolder/odysseus-aio`
2. Install **Odysseus-AIO**
3. Open `http://<your-ip>:9000` for the management UI

### Docker Compose

```bash
docker compose -f docker-compose.aio.yml up -d
```

## Configuration

### Choosing stable vs dev

The AIO pulls the upstream Odysseus image based on the `ODYSSEUS_APP_IMAGE` environment variable:

| Value | Description |
|---|---|
| `realitymolder/odysseus:stable` | Latest stable release (default) |
| `realitymolder/odysseus:dev` | Latest development build |
| `realitymolder/odysseus:YYYY-MM-DD` | Pin to a specific date |

Set it in the Unraid template or in `docker-compose.aio.yml`.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `ODYSSEUS_APP_IMAGE` | `realitymolder/odysseus:stable` | Upstream Odysseus image to deploy |
| `ODYSSEUS_APP_PORT` | `7000` | Host port for Odysseus web UI |
| `ODYSSEUS_CHROMADB_PORT` | `8100` | Host port for ChromaDB |
| `ODYSSEUS_SEARXNG_PORT` | `8080` | Host port for SearXNG |
| `ODYSSEUS_NTFY_PORT` | `8091` | Host port for ntfy |
| `ODYSSEUS_PUID` | `99` | User ID for file permissions |
| `ODYSSEUS_PGID` | `100` | Group ID for file permissions |
| `ODYSSEUS_AUTH_ENABLED` | `true` | Enable authentication |
| `ODYSSEUS_ADMIN_USER` | `admin` | Admin username |
| `ODYSSEUS_ADMIN_PASSWORD` | (auto-generated) | Pre-seed admin password |
| `ODYSSEUS_LLM_HOST` | | Primary LLM server hostname |
| `ODYSSEUS_OPENAI_API_KEY` | | OpenAI API key |
| `ODYSSEUS_OLLAMA_BASE_URL` | | Ollama server URL |
| `ODYSSEUS_NVIDIA_ENABLED` | `false` | Enable NVIDIA GPU passthrough |
| `ODYSSEUS_DNS_SERVERS` | `8.8.8.8,1.1.1.1` | DNS for managed containers |

## Requirements

- Docker socket access (`/var/run/docker.sock`) for managing sibling containers
- For GPU: [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)

## Related repos

| Repo | Purpose |
|---|---|
| [odysseus](https://github.com/realitymolder/odysseus) | Main Odysseus Docker image (stable + dev builds) |
| [odysseus-ca-templates](https://github.com/realitymolder/odysseus-ca-templates) | Unraid CA templates for standalone install |

## License

[MIT](LICENSE)
