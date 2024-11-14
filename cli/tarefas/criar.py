import click
import requests

API_URL="http://127.0.0.1:5000/tarefas"

@click.command()
@click.option('--titulo', prompt='Título da tarefa', help='Título da nova tarefa.')
@click.option('--descricao', prompt='Descrição da tarefa', help='Descrição da nova tarefa.')
def criar(titulo, descricao):
    """Cria uma nova tarefa na API."""
    data = {'titulo': titulo, 'descricao': descricao}
    response = requests.post(f"{API_URL}", json=data)

    if response.status_code == 201:
        click.echo("Tarefa criada com sucesso!")
        click.echo("Response: " + str(response.json()))
    else:
        click.echo(f"Erro ao criar tarefa: {response.json()}")
        
if __name__ == "__main__":
    criar()