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
pash-pipe parse-pashfile    Lê o .pashfile e valida a configuração da aplicação
pash-pipe build             Build da imagem Docker com a tag informada
pash-pipe push              Push da imagem para o registry GHCR
pash-pipe update-image-tag  Atualiza image.tag no values.yaml do ambiente e commita
pash-pipe sync-argocd       Dispara sync da Application no ArgoCD
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
