# Administrator Guide

This guide is for system administrators deploying Species Explorer in enterprise environments.

## Overview

Species Explorer is a QGIS plugin that requires:

- QGIS 3.0 or later
- Network access to GBIF API (`api.gbif.org`)
- Python 3.9+ (bundled with QGIS)

## Deployment Options

### Option 1: QGIS Plugin Repository (Recommended)

For individual workstations:

1. Users install via QGIS Plugin Manager
2. Automatic updates when new versions are released
3. No administrative intervention required

### Option 2: Custom Plugin Repository

For enterprise deployments with controlled software:

1. Download plugin ZIP from [GitHub Releases](https://github.com/kartoza/SpeciesExplorer/releases)
2. Host on internal file server or web server
3. Configure QGIS to use custom repository

**Repository XML Format:**

```xml
<?xml version="1.0"?>
<plugins>
  <pyqgis_plugin name="Species Explorer" version="0.3.0">
    <description>Explore species occurrence data from GBIF</description>
    <about>QGIS plugin for biodiversity data visualization</about>
    <version>0.3.0</version>
    <qgis_minimum_version>3.0</qgis_minimum_version>
    <homepage>https://github.com/kartoza/SpeciesExplorer</homepage>
    <file_name>SpeciesExplorer-0.3.0.zip</file_name>
    <author_name>Kartoza</author_name>
    <download_url>https://your-server/plugins/SpeciesExplorer-0.3.0.zip</download_url>
  </pyqgis_plugin>
</plugins>
```

**QGIS Configuration:**

1. Go to Settings → Options → General → Plugin Repositories
2. Add your custom repository URL
3. Users can install from Plugin Manager

### Option 3: Pre-installed QGIS Profile

For standardized deployments:

1. Create QGIS profile with pre-installed plugins
2. Deploy profile to users via:
   - Roaming profiles (Windows)
   - Configuration management (Ansible, Puppet)
   - Disk imaging

**Profile Location:**

| Platform | Path |
|----------|------|
| Linux | `~/.local/share/QGIS/QGIS3/profiles/` |
| Windows | `%APPDATA%\QGIS\QGIS3\profiles\` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/` |

## Network Requirements

### Firewall Rules

Allow outbound HTTPS (443) to:

| Host | Purpose |
|------|---------|
| `api.gbif.org` | GBIF REST API |
| `www.gbif.org` | GBIF website (optional) |

### Proxy Configuration

Species Explorer uses QGIS native networking, which respects system/QGIS proxy settings.

**Configure in QGIS:**

1. Settings → Options → Network
2. Set proxy type and credentials
3. Species Explorer will use these settings

**Environment Variables:**

```bash
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
export NO_PROXY=localhost,127.0.0.1
```

### SSL/TLS

- GBIF API uses TLS 1.2+
- Ensure CA certificates are up to date
- For corporate SSL inspection, add certificates to system trust store

## Resource Usage

### Network Bandwidth

| Operation | Typical Size |
|-----------|--------------|
| Species search | 1-10 KB |
| Taxonomy lookup | 1-5 KB |
| Occurrence fetch | 100 KB - 50 MB |

**Note:** Large species datasets (millions of records) may download significant data.

### Memory

- Occurrence data is loaded into RAM
- Memory usage scales with record count
- Typical usage: 100 MB per 100,000 records

### Disk

- Plugin installation: ~2 MB
- Downloaded data: Stored in memory, saved to project file

## Security Considerations

### Data Privacy

- No user data is sent to GBIF
- Only species names are transmitted
- Downloaded data may contain location information

### Network Security

- All connections use HTTPS
- No authentication required for GBIF API
- Plugin does not store credentials

### Plugin Security

- Open source (auditable code)
- No external dependencies beyond QGIS
- REUSE compliant licensing

## Monitoring

### Log Files

QGIS logs are available in:

- View → Log Messages panel
- `~/.local/share/QGIS/QGIS3/logs/` (Linux)

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection timeout | Check firewall/proxy |
| SSL errors | Update CA certificates |
| Slow downloads | Normal for large datasets |
| Plugin not loading | Check Python errors in log |

## Batch Deployment

### Windows (PowerShell)

```powershell
$pluginPath = "$env:APPDATA\QGIS\QGIS3\profiles\default\python\plugins"
$pluginUrl = "https://github.com/kartoza/SpeciesExplorer/releases/latest/download/SpeciesExplorer.zip"

# Download and extract
Invoke-WebRequest -Uri $pluginUrl -OutFile "$env:TEMP\SpeciesExplorer.zip"
Expand-Archive -Path "$env:TEMP\SpeciesExplorer.zip" -DestinationPath $pluginPath -Force
```

### Linux (Bash)

```bash
#!/usr/bin/env bash
PLUGIN_PATH="$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
PLUGIN_URL="https://github.com/kartoza/SpeciesExplorer/releases/latest/download/SpeciesExplorer.zip"

mkdir -p "$PLUGIN_PATH"
curl -L "$PLUGIN_URL" -o /tmp/SpeciesExplorer.zip
unzip -o /tmp/SpeciesExplorer.zip -d "$PLUGIN_PATH"
```

### Ansible Playbook

```yaml
---
- name: Install Species Explorer plugin
  hosts: workstations
  tasks:
    - name: Download plugin
      get_url:
        url: https://github.com/kartoza/SpeciesExplorer/releases/latest/download/SpeciesExplorer.zip
        dest: /tmp/SpeciesExplorer.zip

    - name: Extract plugin
      unarchive:
        src: /tmp/SpeciesExplorer.zip
        dest: "{{ ansible_env.HOME }}/.local/share/QGIS/QGIS3/profiles/default/python/plugins/"
        remote_src: yes
```

## Troubleshooting

### Plugin Won't Load

1. Check QGIS version (3.0+ required)
2. Check Python version (3.9+ recommended)
3. Review QGIS log for errors
4. Verify plugin is enabled in Plugin Manager

### Network Issues

1. Test connectivity: `curl https://api.gbif.org/v1/species/1`
2. Check proxy settings in QGIS
3. Verify firewall rules
4. Test SSL: `openssl s_client -connect api.gbif.org:443`

### Performance Issues

1. Large datasets are expected to be slow
2. Consider filtering data after import
3. Use SSD for QGIS projects
4. Allocate sufficient RAM

## Support

- **Documentation:** [https://kartoza.github.io/SpeciesExplorer](https://kartoza.github.io/SpeciesExplorer)
- **Issues:** [GitHub Issues](https://github.com/kartoza/SpeciesExplorer/issues)
- **Commercial Support:** [Kartoza](https://kartoza.com)

---

Made with 💗 by [Kartoza](https://kartoza.com) | [Donate](https://github.com/sponsors/timlinux) | [GitHub](https://github.com/kartoza/SpeciesExplorer)
