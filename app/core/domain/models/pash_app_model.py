from dataclasses import dataclass, field
from typing import Dict, List, Optional


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
class QualityConfig:
    runtime: str
    workdir: str
    install_command: Optional[str] = None
    fmt_command: Optional[str] = None
    lint_command: Optional[str] = None
    test_command: Optional[str] = None
    cover_command: Optional[str] = None
    build_command: Optional[str] = None
    lint_config: Optional[str] = None
    cover_config: Optional[str] = None
    ignore_patterns: List[str] = field(default_factory=list)
    coverage_threshold: int = 90


@dataclass
class PashAppModel:
    sigla: str
    app_name: str
    repo: str
    helm: HelmConfig
    type: Optional[str] = field(default=None)
    shortname: Optional[str] = field(default=None)
    quality: Optional[QualityConfig] = field(default=None)
