import click
import requests
import os

@click.command()
@click.option('--titulo', prompt='Título da tarefa', help='Título da nova tarefa.')
@click.option('--descricao', prompt='Descrição da tarefa', help='Descrição da nova tarefa.')
def criar(titulo, descricao):
    """Cria uma nova tarefa na API."""
    data = {'titulo': titulo, 'descricao': descricao}
    response = requests.post(os.getenv('API_URL'), json=data)

    if response.status_code == 201:
        click.echo("Tarefa criada com sucesso!")
    else:
        click.echo(f"Erro ao criar tarefa: {response.json()}")
        
if __name__ == "__main__":
    criar()