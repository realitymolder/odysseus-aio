# Pushing Docker Images to Docker Hub from GitHub Actions

## One-Time Setup

### 1. Create a Docker Hub Access Token

1. Log in to [hub.docker.com](https://hub.docker.com)
2. Go to **Account Settings → Security → Access Tokens**
3. Click **New Access Token**
   - Description: `GitHub Actions`
   - Access permissions: **Read & Write**
4. Click **Generate**
5. **Copy the token immediately** — it won't be shown again

### 2. Add GitHub Repository Secrets

For each repo that pushes images (`odysseus`, `odysseus-aio`):

1. Go to the repo on GitHub
2. **Settings → Secrets and variables → Actions**
3. Click **New repository secret** and add:

| Name | Value |
|------|-------|
| `DOCKERHUB_USERNAME` | `realitymolder` |
| `DOCKERHUB_TOKEN` | The token from step 1 |

## How the Workflow Works

### Login Step

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@v3
  with:
    username: ${{ secrets.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_TOKEN }}
```

This authenticates the Docker client for the rest of the job. No `docker login` command needed — the action handles it.

### Build and Push Step

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v6
  with:
    context: .
    file: ./Dockerfile
    push: true            # <-- this pushes to Docker Hub
    tags: ${{ steps.meta.outputs.tags }}
    labels: ${{ steps.meta.outputs.labels }}
```

When `push: true` is set, the image is pushed to the registry specified in the login step (Docker Hub in this case). The image name comes from the `tags` input.

### Tag Metadata Step

```yaml
- name: Extract metadata for Docker
  id: meta
  uses: docker/metadata-action@v5
  with:
    images: realitymolder/odysseus    # <-- Docker Hub image name
    tags: |
      type=raw,value=stable,enable={{is_default_branch}}
      type=raw,value={{date 'YYYY-MM-DD'}},enable={{is_default_branch}}
```

The `images` field sets the base image name (Docker Hub username/repo). Tags are generated from the rules. The `metadata-action` outputs `tags` and `labels` consumed by `build-push-action`.

### Tag Strategy

| Trigger | Branch | Docker Hub Tags | Example |
|---------|--------|-----------------|---------|
| Push to `main` | `main` | `stable`, `YYYY-MM-DD` | `realitymolder/odysseus:stable`, `realitymolder/odysseus:2026-06-20` |
| Daily schedule | `dev` | `dev`, `dev-YYYY-MM-DD` | `realitymolder/odysseus:dev`, `realitymolder/odysseus:dev-2026-06-20` |
| Manual dispatch | configurable | custom tag | `realitymolder/odysseus:test` |

## Full Workflow Example

```yaml
name: Build and push Odysseus Docker image

on:
  push:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'          # daily at 06:00 UTC
  workflow_dispatch:
    inputs:
      upstream_branch:
        description: 'Upstream branch to build'
        required: false
        default: 'dev'
        type: choice
        options: ['main', 'dev']
      custom_tag:
        description: 'Custom tag (optional)'
        required: false
        type: string

env:
  IMAGE_NAME: realitymolder/odysseus

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read

    steps:
      - name: Checkout upstream
        uses: actions/checkout@v4
        with:
          repository: pewdiepie-archdaemon/odysseus
          ref: ${{ inputs.upstream_branch || (github.event_name == 'schedule' && 'dev' || 'main') }}

      - name: Log in to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Determine tags
        id: tags
        run: |
          if [ "${{ github.event_name }}" = "schedule" ]; then
            echo "tags=dev,dev-$(date +'%Y-%m-%d')" >> "$GITHUB_OUTPUT"
          elif [ "${{ github.ref }}" = "refs/heads/main" ]; then
            echo "tags=stable,$(date +'%Y-%m-%d')" >> "$GITHUB_OUTPUT"
          elif [ -n "${{ inputs.custom_tag }}" ]; then
            echo "tags=${{ inputs.custom_tag }}" >> "$GITHUB_OUTPUT"
          else
            echo "tags=dev" >> "$GITHUB_OUTPUT"
          fi

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: .
          file: ./Dockerfile
          push: true
          tags: ${{ env.IMAGE_NAME }}:${{ steps.tags.outputs.tags }}
          build-args: |
            INSTALL_OPTIONAL=false
```

## Pulling the Images

After pushing, users pull with:

```bash
# Stable (latest release)
docker pull realitymolder/odysseus:stable

# Specific date
docker pull realitymolder/odysseus:2026-06-20

# Dev (latest development)
docker pull realitymolder/odysseus:dev

# AIO
docker pull realitymolder/odysseus-aio:latest
```

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `unauthorized` | Token missing or expired | Regenerate token, update GitHub secret |
| `denied: requested access to the resource is denied` | Wrong username or repo doesn't exist on Docker Hub | Create the repo on Docker Hub first, or let `push: true` create it (requires auto-create enabled) |
| `name unknown: repository does not exist` | Image repo not found | Go to hub.docker.com → Create repository with the same name |
