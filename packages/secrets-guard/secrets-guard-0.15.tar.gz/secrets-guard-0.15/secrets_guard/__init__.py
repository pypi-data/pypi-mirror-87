from pathlib import Path


APP_NAME = "secrets-guard"
APP_VERSION = "0.15"
STORE_EXTENSION = ".sec"
KEYRING_EXTENSION = ".skey"
DEFAULT_SECRETS_PATH = Path.home() / ".secrets"
DATETIME_FORMAT = "%d/%m/%Y %H:%M:%S"