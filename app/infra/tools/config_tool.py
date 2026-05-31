import os


class ConfigTool:
    @property
    def github_token(self) -> str:
        return self._require("GITHUB_TOKEN")

    @property
    def argocd_url(self) -> str:
        return self._require("ARGOCD_URL")

    @property
    def argocd_token(self) -> str:
        return self._require("ARGOCD_TOKEN")

    @property
    def registry(self) -> str:
        return self._require("REGISTRY")

    @property
    def argocd_insecure(self) -> bool:
        return os.environ.get("ARGOCD_INSECURE", "false").lower() == "true"

    def _require(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise EnvironmentError(f"Variável de ambiente obrigatória não definida: {key}")
        return value
