from dataclasses import dataclass
from typing import Dict


@dataclass
class EnvironmentConfig:
    values_file: str


@dataclass
class HelmConfig:
    chart_repo: str
    chart_name: str
    chart_version: str
    environments: Dict[str, EnvironmentConfig]


@dataclass
class PashAppModel:
    sigla: str
    app_name: str
    repo: str
    helm: HelmConfig
