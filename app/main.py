from infra.init.ioc_init import IocInit


def cli():
    ioc = IocInit()
    cli_init = ioc.get_cli_init()
    cli_init.run()


if __name__ == "__main__":
    cli()
