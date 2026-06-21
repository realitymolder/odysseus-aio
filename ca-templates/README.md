# Odysseus CA Templates

Unraid Community Applications templates for [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) AI workspace and related services.

## Templates

| Template | Description |
|---|---|
| `odysseus.xml` | Main Odysseus AI workspace (standalone install, requires companion containers) |
| `odysseus-aio.xml` | Odysseus AIO master container (all-in-one, auto-deploys full stack) |
| `chromadb.xml` | ChromaDB vector database (companion for standalone Odysseus) |

## Adding to Unraid

1. Go to **Community Applications → Settings → Repositories**
2. Add this repository URL:
   ```
   https://github.com/realitymolder/odysseus-ca-templates
   ```
3. Templates will appear under the **Odysseus** category

## Adding New Templates

1. Create an XML file following the [Unraid Docker Template XML Schema](https://forums.unraid.net/topic/38619-docker-template-xml-schema/)
2. Add a 192x192 PNG icon to `templates/img/`
3. Submit a pull request

### Template guidelines

- Use lowercase, hyphenated filenames (e.g. `my-app.xml`)
- Include `<Registry>` pointing to the Docker Hub or GHCR page
- Include `<Support>` and `<Project>` links
- Icon should be 192x192 PNG or SVG

## Links

- [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus)
- [Unraid Docker Template XML Schema](https://forums.unraid.net/topic/38619-docker-template-xml-schema/)
- [Writing a template compatible for Unraid](https://selfhosters.net/docker/templating/templating/)
