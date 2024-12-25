# Matey Exporter

A Prometheus exporter for collecting and exposing metrics from Matey services.

## Description

Prometheus Matey Exporter enables monitoring of services used by virtual sailors of the seven seas, by collecting relevant metrics and exposing them in Prometheus format. This makes it easy to integrate Matey service monitoring into your existing Prometheus ecosystem.

The main difference from other Prometheus exporters is that Matey Exporter is designed to work with multiple services from a single exporter instance, as well as support a wider variety of services.

The project is still in early stages and missing a lot of supported metrics. Feel free to contribute and help improve it.

Currently supported services metrics and tested versions:
| Service  | Version |
|   ---    |  ---    |
| Radarr   |  ---    |
| Sonarr   |  ---    |
| Lidarr   |  ---    |
| Readarr  |  ---    |
| Prowlarr |  ---    |
| qBittorrent | 5.0.3  |
| Transmission| ---  |
| Deluge  |   2.1.1  |

## Installation

To get started with matey_exporter, you’ll need Python or Docker installed. This project is tested with Python >=3.10.

#### Requirements

Python >=3.10

`pip` for installing dependencies.

Install dependencies in `requirements.txt`

## Usage
Clone the repository and install the required dependencies.

```bash
git clone https://github.com/therealscienta/matey_exporter.git
cd matey_exporter
```
Edit configuration file `config.yml`

### As Python Script

Install dependencies:
```bash
pip install -r requirements.txt
```
Edit configuration file `config.yml` and then start the app by running `python app.py`.

### From Makefile
(Only tested on Debian)

By using the make file the exporter is compiled using Pyinstaller and installed on the system as a runnable service.

Edit configuration file `config.yml` and then run: `make install`.

### As [Docker container](https://hub.docker.com/r/therealscienta/matey_exporter)

Inside the directory, run the following command:
```bash
docker run -d -p 8000:8000 -v ./config.yaml:/app/config.yaml matey_exporter:latest
```

Or as a compose file:
```bash
docker compose up -d
```

To run latest development image, use `dev-latest`

## Configuration
[Configuration details will be added]

## Data collection agent

Configuration snippets for data collecting agents.

Grafana Alloy:
```
prometheus.scrape "matey" {
  forward_to = [prometheus.remote_write.<prometheus_remote_write_component_name>.receiver,]
  scrape_interval = "30s"
  targets = [
    {
      "__address__" = "localhost:8000",
      "job" = "matey",
    },
  ]
}
```

Prometheus node exporter:

```yaml
scrape_configs:
- job_name: 'matey'
  scrape_interval: 30s
  static_configs:
  - targets: ['localhost:8000']
```


## Development
To contribute to this project:

Fork the repository

1. Create your feature branch
2. Commit your changes
3. Push to the branch
4. Create a new Merge Request

## Testing
[Testing instructions will be added]

Run `pytest` to run the test suite.

## Support
For support, please:

Open an issue in the GitLab repository
Contact the maintainers

## Roadmap
* Initial exporter implementation
* Basic metrics collection
* Configuration options
* Documentation
* Testing suite
* CI/CD pipeline

## License

[MIT License](LICENSE)

## Project Status
Active development - Early stages

## Contributing
Contributions are welcome! Please read our contributing guidelines before submitting merge requests.

For more information about setting up Prometheus exporters, visit the official Prometheus documentation.
