# Odysseus Unraid Community App — Tasks

## Phase 1: Repository setup

- [ ] Push this repo to a GitHub account
- [ ] In repo Settings → Actions → General: enable "Allow all actions"
- [ ] In repo Settings → Actions → General: set Workflow permissions to "Read and write permissions"
- [ ] Push to `main` to trigger `.github/workflows/docker-publish.yml`
- [ ] Verify the Action runs successfully and a GHCR package appears under the repo Packages section
- [ ] Make the GHCR package public: Packages → select package → Package settings → Change visibility to public

## Phase 2: GitHub Actions & Docker image

- [ ] In repo Settings → Actions → General: enable "Allow all actions"
- [ ] In repo Settings → Actions → General: set Workflow permissions to "Read and write permissions"
- [ ] Push to `main` to trigger `.github/workflows/docker-publish.yml`
- [ ] Verify the Action runs successfully and a GHCR package appears under repo → Packages
- [ ] Make the GHCR package public: Packages → select the package → Package settings → Change visibility to public

## Phase 3: Install on Unraid

- [ ] Install ChromaDB companion: Apps → search "Odysseus-ChromaDB" → install
- [ ] Install SearXNG companion: Apps → search "Odysseus-SearXNG" → install
- [ ] Install ntfy companion: Apps → search "Odysseus-ntfy" → install
- [ ] Install the main Odysseus app: Apps → search "Odysseus" → install
- [ ] Verify all four containers are running in Docker tab
- [ ] Verify all containers are running in Docker tab
- [ ] Check Odysseus logs for auto-generated admin password
- [ ] Log in at `http://<unraid-ip>:7000`
- [ ] Change the default admin password in Settings
- [ ] Configure LLM provider (Ollama, OpenAI, or local endpoint) in Settings

## Phase 4: Submit to Unraid Community Apps

- [ ] Visit https://ca.unraid.net/submit and read the guidelines
- [ ] Fork https://github.com/community-apps/unraid-community-apps
- [ ] Add the `ca_profile.xml` URL pointing to your repo
- [ ] Submit a pull request to the unraid-community-apps repo
- [ ] Wait for moderator review and address any feedback

## Phase 5: Ongoing maintenance

- [ ] Optional: enable NVIDIA GPU passthrough (`--runtime=nvidia` + `NVIDIA_VISIBLE_DEVICES=all`)
- [ ] Update the Odysseus image by re-running the GH Action workflow on demand
- [ ] Remove `session-ses_1672.md` before committing to GitHub
