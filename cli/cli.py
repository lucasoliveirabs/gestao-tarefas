import click
from tarefas.criar import criar
from tarefas.listar import listar
from tarefas.alterar import alterar
from tarefas.excluir import excluir

API_URL="http://127.0.0.1:5000/tarefas"

@click.group()
def cli():
    """CLI cliente da API gestão de tarefas."""
    pass

cli.add_command(criar)
cli.add_command(listar)
cli.add_command(alterar)
cli.add_command(excluir)

if __name__ == "__main__":
    cli()