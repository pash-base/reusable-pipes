import click
from interfaces.core.application.i_parse_pashfile_use_case import IParsePashfileUseCase
from interfaces.core.application.i_build_image_use_case import IBuildImageUseCase
from interfaces.core.application.i_push_image_use_case import IPushImageUseCase
from interfaces.core.application.i_update_image_tag_use_case import IUpdateImageTagUseCase
from interfaces.core.application.i_sync_argocd_use_case import ISyncArgoCDUseCase
from infra.tools.logger_tool import LoggerTool


class CliInit:
    def __init__(
        self,
        parse_uc: IParsePashfileUseCase,
        build_uc: IBuildImageUseCase,
        push_uc: IPushImageUseCase,
        update_uc: IUpdateImageTagUseCase,
        sync_uc: ISyncArgoCDUseCase,
        logger: LoggerTool,
    ):
        self._parse_uc = parse_uc
        self._build_uc = build_uc
        self._push_uc = push_uc
        self._update_uc = update_uc
        self._sync_uc = sync_uc
        self._logger = logger

    def run(self):
        @click.group()
        def cli():
            pass

        @cli.command("parse-pashfile")
        @click.option("--path", default=".pashfile", help="Caminho para o .pashfile")
        def parse_pashfile(path):
            result = self._parse_uc.execute(path)
            click.echo(result)

        @cli.command("build")
        @click.option("--tag", required=True, help="Tag da imagem (ex: SHA do commit)")
        @click.option("--path", default=".pashfile", help="Caminho para o .pashfile")
        def build(tag, path):
            app = self._parse_uc.execute(path)
            self._build_uc.execute(app=app, tag=tag)

        @cli.command("push")
        @click.option("--tag", required=True, help="Tag da imagem")
        @click.option("--path", default=".pashfile", help="Caminho para o .pashfile")
        def push(tag, path):
            app = self._parse_uc.execute(path)
            self._push_uc.execute(app=app, tag=tag)

        @cli.command("update-image-tag")
        @click.option("--env", required=True, type=click.Choice(["dev", "hom", "prd"]))
        @click.option("--tag", required=True, help="Nova tag da imagem")
        @click.option("--path", default=".pashfile", help="Caminho para o .pashfile")
        def update_image_tag(env, tag, path):
            app = self._parse_uc.execute(path)
            self._update_uc.execute(app=app, env=env, tag=tag)

        @cli.command("sync-argocd")
        @click.option("--app-name", required=True, help="Nome da Application ArgoCD")
        def sync_argocd(app_name):
            self._sync_uc.execute(app_name=app_name)

        cli()
