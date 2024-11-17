from pathlib import Path

class MateyExporterConfig:
    DEFAULT_CONFIG_FILE = Path(Path(__file__).parent.parent) / 'config.yaml'
    DEFAULT_LOGLEVEL = 'INFO'
    DEFAULT_PORT = 8000
    DEFAULT_INTERVAL = 30