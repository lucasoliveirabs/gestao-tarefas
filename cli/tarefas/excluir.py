import click
import requests

API_URL = "http://127.0.0.1:5000/tarefas"

@click.command()
@click.option('--id', prompt='ID da tarefa', help='ID da tarefa a ser excluída.')
def excluir(id):
    """Exclui uma tarefa existente na API."""
    data = {"id": id}
    response = requests.delete(f"{API_URL}", json=data)
    
    if response.status_code == 200:
        click.echo("Tarefa excluída com sucesso!")
        click.echo("Response: " + str(response.json()))
    elif response.status_code == 404:
        click.echo("Erro: Tarefa não encontrada.")
    else:
        click.echo(f"Erro ao excluir a tarefa: {response.json()}")

if __name__ == "__main__":
    excluir()