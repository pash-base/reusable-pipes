# Changelog

Todas as mudanças relevantes deste projeto serão documentadas neste arquivo.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
seguindo [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Adicionado

- **`ResolveAppNamesUseCase`**: novo use case que resolve os nomes semânticos de uma aplicação por ambiente, seguindo o padrão `<sigla_lower>-<type>-<shortname>-<env>`.
- **`PashAppModel`**: novos campos `type` e `shortname`, derivados automaticamente de `metadata.repo` no Pashfile (padrão `pash-<SIGLA>-<type>-<shortname>`).
- **CLI `resolve-app-names`**: novo subcomando com suporte às flags `--path`, `--env` e `--output` (`json` ou `text`).
- **`QualityConfig`**: novo dataclass no modelo de domínio com 12 campos de configuração de qualidade (`runtime`, `workdir`, `installCommand`, `fmtCommand`, `lintCommand`, `testCommand`, `coverCommand`, `buildCommand`, `lintConfig`, `coverConfig`, `ignorePatterns`, `coverageThreshold`).
- **6 novos use cases de qualidade**: `InstallUseCase`, `FmtUseCase`, `LintUseCase`, `TestUseCase`, `CoverUseCase`, `ValidateUseCase` — todos leem configuração do `.pashfile` via `QualityConfig`.
- **6 novos subcomandos CLI**: `install`, `fmt`, `lint`, `test`, `cover`, `validate` — todos aceitam a flag `--path` e delegam execução ao use case correspondente.
- **Suporte a `spec.pipeline.runtime` no `.pashfile`**: bloco completo de configuração de qualidade com os campos do `QualityConfig` disponíveis para declarar comandos, configs de linter/cobertura, padrões de ignore e threshold de cobertura.

### Corrigido

- **`develop-cd.yml`**: corrigido path relativo inválido na instalação do `pash-pipe` (era `../reusable-pipes/app`; agora usa `git clone` do repositório).
- **`develop-cd.yml`**: adicionado parâmetro `--branch develop` obrigatório na chamada de `update-image-tag`.
- **`develop-cd.yml`**: substituído `--app-name portal-platform-dev` hardcoded por chamada dinâmica ao `resolve-app-names`.
- **4 workflows reutilizáveis**: substituídos steps simulados (`echo`/`sleep`) por chamadas reais ao `pash-pipe`.

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
