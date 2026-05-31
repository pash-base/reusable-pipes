# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
seguindo [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [0.2.0] - 2025-01-01

### Alterado

- **`update-image-tag`**: o parâmetro `--branch` passou a ser **obrigatório** na CLI e no contrato de interface `IUpdateImageTagUseCase.execute()`.
  - **Antes:** a branch era derivada automaticamente do ambiente (`dev` → `develop`, `hom` → `release/current`, `prd` → `master`), com o valor `release/current` hardcoded para o ambiente `hom`.
  - **Depois:** o chamador informa explicitamente a branch de destino via `--branch <branch>`, tornando o pipeline compatível com qualquer estratégia de branching (ex: `release/v1.0.0`, `release/v2.0.0`).

### Motivação

A lógica hardcoded `release/current` para o ambiente `hom` era incompatível com fluxos GitOps baseados em branches de release versionadas (ex: `release/v1.0.0`). A mudança delega a decisão de branch para o pipeline de CD da aplicação, que conhece a branch correta para cada execução.

### Migração

Pipelines que chamavam `update-image-tag` sem `--branch` devem ser atualizados:

```yaml
# antes
- run: pash-pipe update-image-tag --env hom --tag ${{ env.TAG }}

# depois
- run: pash-pipe update-image-tag --env hom --tag ${{ env.TAG }} --branch release/v1.0.0
```

---

## [0.1.0] - 2025-01-01

### Adicionado

- CLI `pash-pipe` com 5 subcomandos: `parse-pashfile`, `build`, `push`, `update-image-tag`, `sync-argocd`.
- Implementação com Clean Architecture: camadas `adapters`, `core`, `infra`, `interfaces`.
- Clientes: `ArgocdClient`, `GithubClient`.
- Repositório: `PashfileRepository` (leitura do `.pashfile` YAML).
- Use cases: `ParsePashfileUseCase`, `BuildUseCase`, `PushUseCase`, `UpdateImageTagUseCase`, `SyncArgoCDUseCase`.
- Ferramentas de infraestrutura: `LoggerTool`, `ConfigTool`.
- Testes unitários com cobertura ≥ 90%.
- Makefile com targets: `install`, `fmt`, `lint`, `test`, `cover`, `validate`.
