# Docker Compose Maintenance

When upstream [Odysseus](https://github.com/pewdiepie-archdaemon/odysseus) adds new environment variables, changes service dependencies, or modifies ports, update `docker-compose.yml` to match — otherwise compose-based installs will miss new config options.

Periodically diff your compose file against the upstream repo's recommended setup and merge any new variables or structural changes.
