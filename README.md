# Odysseus Unraid Community App

[Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) is a self-hosted AI workspace — chat, agents, deep research, documents, email, calendar, and model Cookbook. This repository provides the Unraid Community Applications (CA) templates to run Odysseus on your Unraid server.

## ⚠️ Prerequisites

These templates require a **prebuilt Docker image** on GitHub Container Registry. An automated GitHub Action in this repo builds and publishes the image automatically.

### Setup for first-time use

1. **Fork or push this repo** to your own GitHub account
2. **Enable GitHub Actions** in your repo settings (Settings → Actions → General → Allow all actions)
3. **Enable package creation**: Settings → Actions → General → Workflow permissions → "Read and write permissions" + "Allow GitHub Actions to create and approve pull requests"
4. **Push to `main`** — the workflow in `.github/workflows/docker-publish.yml` will build and push the image to `ghcr.io/realitymolder/odysseus-unraid:latest`
5. **Make the package public**: Go to your repo → Packages → select the package → Package settings → Change visibility to public

## Templates

| Template | Container | Required? | Description |
|---|---|---|---|---|
| `templates/odysseus.xml` | Odysseus | Yes | Main AI workspace app |
| `templates/odysseus-chromadb.xml` | ChromaDB | Yes | Vector store for memory |
| `templates/odysseus-searxng.xml` | SearXNG | Yes | Meta search engine |
| `templates/odysseus-ntfy.xml` | ntfy | Yes | Notifications |

## Installation via Unraid Community Apps

CA's dependency system enforces the install order — install **Odysseus** and all three required companions are automatically prompted.

1. Add this repository to CA: **Apps** → **Settings** → **Template Repositories** → Add `https://github.com/realitymolder/Odysseus-Unraid`
2. Install **Odysseus-ChromaDB**
3. Install **Odysseus-SearXNG**
4. Install **Odysseus-ntfy**
5. Install **Odysseus** (main app)

### Container naming

The main Odysseus container connects to companions using Docker internal hostnames. Ensure the companion containers are named exactly:
- `odysseus-chromadb`
- `odysseus-searxng`
- `odysseus-ntfy`

The template defaults are preconfigured for these names.

## Post-install

1. Open the Odysseus WebUI at `http://<your-unraid-ip>:7000`
2. Find the auto-generated admin password in the container logs: **Docker** → select Odysseus container → **Logs**
3. Log in with username `admin` (or the value of `ODYSSEUS_ADMIN_USER`)
4. Change the password in **Settings**
5. Configure your LLM provider in **Settings** → add Ollama, OpenAI, or a local endpoint

## GPU passthrough (optional)

For NVIDIA GPUs, install the **NVIDIA Container Toolkit** on your Unraid host via the Nvidia Drivers plugin, then add these extra parameters to the Odysseus container template:

```
--runtime=nvidia
-e NVIDIA_VISIBLE_DEVICES=all
```

## Updating

- **Odysseus image**: Run the GitHub Action workflow manually, then **Apps** → **Previous Apps** → reinstall or **Docker** → force update the container.
- **Companion containers**: Update through the Unraid Docker page as usual.

## Submitting to Unraid Community Apps

Once your repository is ready:

1. Go to [ca.unraid.net/submit](https://ca.unraid.net/submit)
2. Fork the [unraid-community-apps](https://github.com/community-apps/unraid-community-apps) repo
3. Add your `ca_profile.xml` URL to the appropriate location
4. Submit a pull request

See the [official docs](https://ca.unraid.net/submit/help/repository-xml) for detailed submission guidelines.

## License

Templates: MIT  
Odysseus: [MIT](https://github.com/pewdiepie-archdaemon/odysseus/blob/dev/LICENSE)
