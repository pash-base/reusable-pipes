from dataclasses import dataclass, field
from typing import Dict, Optional


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
    type: Optional[str] = field(default=None)
    shortname: Optional[str] = field(default=None)
