import click, os
from tarefas.criar import criar
from tarefas.listar import listar
from tarefas.alterar import alterar
from tarefas.excluir import excluir

@click.group()
def cli():
    """Bem-vindo ao CLI de Gestão de Tarefas!"""
    click.echo("")
    click.echo("===============================================")
    click.echo("Comandos possíveis abaixo. Use --help para conferir as opções disponíveis.")
    click.echo("")
    click.echo("  listar                -> Lista todas as tarefas")
    click.echo("  criar --titulo ...    -> Cria uma nova tarefa com o título especificado")
    click.echo("  alterar --id ...      -> Altera uma tarefa existente")
    click.echo("  excluir --id ...      -> Exclui uma tarefa")
    click.echo("===============================================")
    click.echo("")

cli.add_command(criar)
cli.add_command(listar)
cli.add_command(alterar)
cli.add_command(excluir)

if __name__ == "__main__":
    cli()