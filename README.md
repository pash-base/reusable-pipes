# reusable-pipes

CLI `pash-pipe` — pipelines de CD reutilizáveis da plataforma Path Shards.

## Sobre

O `pash-pipe` automatiza o ciclo de entrega contínua: parse do `.pashfile`, build e push de imagem Docker, atualização de tag no repositório da aplicação e sincronização do ArgoCD.

## Instalação

```bash
cd app
make install   # pip install -e .
```

## Subcomandos

```
pash-pipe parse-pashfile     Lê o .pashfile e valida a configuração da aplicação
pash-pipe build              Build da imagem Docker com a tag informada
pash-pipe push               Push da imagem para o registry GHCR
pash-pipe update-image-tag   Atualiza image.tag no values.yaml do ambiente e commita
pash-pipe sync-argocd        Dispara sync da Application no ArgoCD
pash-pipe resolve-app-names  Resolve os nomes semânticos da aplicação por ambiente a partir do Pashfile
```

### update-image-tag

```bash
pash-pipe update-image-tag \
  --env <dev|hom|prd> \
  --tag <nova-tag> \
  --branch <branch-git-destino> \
  [--path <caminho-pashfile>]
```

| Opção | Obrigatório | Descrição |
|-------|------------|-----------|
| `--env` | ✅ | Ambiente alvo: `dev`, `hom` ou `prd` |
| `--tag` | ✅ | Nova tag da imagem (ex: SHA do commit) |
| `--branch` | ✅ | Branch Git de destino para o commit GitOps (ex: `develop`, `release/v1.0.0`, `master`) |
| `--path` | ❌ | Caminho para o `.pashfile` (default: `.pashfile`) |

**Exemplos por ambiente:**

```bash
# dev → branch develop
pash-pipe update-image-tag --env dev --tag abc1234 --branch develop

# hom → branch release/v1.0.0
pash-pipe update-image-tag --env hom --tag abc1234 --branch release/v1.0.0

# prd → branch master
pash-pipe update-image-tag --env prd --tag v1.0.0 --branch master
```

### resolve-app-names

```bash
pash-pipe resolve-app-names \
  [--path <caminho-pashfile>] \
  [--env <dev|hom|prd>] \
  [--output <json|text>]
```

| Opção | Obrigatório | Descrição |
|-------|------------|-----------|
| `--path` | ❌ | Caminho para o Pashfile (default: `pashfile.yaml`) |
| `--env` | ❌ | Ambiente específico (`dev`, `hom` ou `prd`). Se omitido, retorna todos os ambientes |
| `--output` | ❌ | Formato de saída: `json` (default) ou `text` |

**Exemplos:**

```bash
# Retorna todos os ambientes em JSON (formato padrão)
pash-pipe resolve-app-names --path pashfile.yaml

# Retorna apenas o ambiente de homologação em texto
pash-pipe resolve-app-names --env hom --output text
```

**Saída esperada (JSON):**

```json
{
  "dev": "doc-portal-platform-dev",
  "hom": "doc-portal-platform-hom",
  "prd": "doc-portal-platform-prd"
}
```

## Convenção de nomes semânticos

O `resolve-app-names` gera nomes no padrão:

```
<sigla_lower>-<type>-<shortname>-<env>
```

Os campos `type` e `shortname` são derivados automaticamente do campo `metadata.repo` no Pashfile, que segue o padrão `pash-<SIGLA>-<type>-<shortname>`:

| Campo no Pashfile | Valor derivado |
|-------------------|----------------|
| `metadata.repo: pash-DOC-portal-platform` | `type: portal`, `shortname: platform` |
| `metadata.repo: pash-API-service-users` | `type: service`, `shortname: users` |

**Exemplo completo:**

Pashfile:

```yaml
metadata:
  sigla: DOC
  repo: pash-DOC-portal-platform
helm:
  environments:
    - dev
    - hom
    - prd
```

Nomes gerados pelo `resolve-app-names`:

```
doc-portal-platform-dev
doc-portal-platform-hom
doc-portal-platform-prd
```

## Variáveis de ambiente obrigatórias

| Variável | Descrição |
|----------|-----------|
| `GITHUB_TOKEN` | Token PAT com permissão de push no repositório da aplicação |
| `ARGOCD_URL` | URL base do ArgoCD (ex: `http://argocd.local`) |
| `ARGOCD_TOKEN` | Token de API do ArgoCD |
| `REGISTRY` | Registry de imagens (ex: `ghcr.io`) |
| `ARGOCD_INSECURE` | `true` para desabilitar verificação TLS (default: `false`) |

## Desenvolvimento

```bash
cd app
make fmt       # formata com black
make lint      # analisa com flake8
make test      # executa testes unitários
make cover     # cobertura de linhas (mínimo: 90%)
make validate  # executa fmt → lint → test → cover em sequência
```

## Estrutura

```
app/
├── main.py                      # entrypoint CLI (excluído da cobertura)
├── setup.cfg                    # metadados e dependências
├── adapters/
│   ├── clients/                 # ArgocdClient, GithubClient
│   └── repositories/            # PashfileRepository
├── core/
│   ├── application/             # use cases
│   └── domain/models/           # PashAppModel, HelmConfig, EnvironmentConfig
├── infra/
│   ├── init/                    # ioc_init.py, cli_init.py (excluídos da cobertura)
│   └── tools/                   # LoggerTool, ConfigTool
├── interfaces/                  # abstrações (ILoggerTool, IConfigTool, etc.)
└── tests/unit/                  # espelha a estrutura de camadas
```
