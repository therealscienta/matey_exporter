# Prometheus Matey Exporter

A Prometheus exporter for collecting and exposing metrics from Matey services.

## Description

Prometheus Matey Exporter enables monitoring of services used by those sailing the virtual seven seas, by collecting relevant metrics and exposing them in Prometheus format. This makes it easy to integrate Matey service monitoring into your existing Prometheus ecosystem.

The project is still in early stages and missing a lot of supported metrics. Feel free to contribute and help improve it.

Currently implemented metrics:
* Radarr
* Sonarr

## Installation

To get started with matey_exporter, you’ll need Python installed. This project is compatible with Python 3.11+.

#### Requirements

Python 3.11+

`pip` for installing dependencies.

Install dependencies in `requirements.txt`

Clone the repository and install the required dependencies.

```bash
git clone https://github.com/therealscienta/matey_exporter.git
cd matey_exporter 
```

## Usage
[Explain how to use your project, with examples if possible]

[Usage instructions will be added as the project develops]

Run the exporter by running the following command:
```bash
python app.py
```

## Configuration
[Configuration details will be added]

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
