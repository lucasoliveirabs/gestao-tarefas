import click
import requests

API_URL = "http://127.0.0.1:5000/tarefas"

@click.command()
@click.option('--id', prompt='ID da tarefa', help='ID da tarefa a ser alterada.')
@click.option('--titulo', help='Novo título da tarefa.')
@click.option('--descricao', help='Nova descrição da tarefa.')
@click.option('--concluida', type=bool, help='Define se a tarefa está concluída. Booleano (True ou False).')
def alterar(id, titulo, descricao, concluida):
    """Altera uma tarefa existente na API."""
    data = {"id": id}
    if titulo:
        data["titulo"] = titulo
    if descricao:
        data["descricao"] = descricao
    if concluida is not None:
        data["concluida"] = concluida
    
    response = requests.patch(f"{API_URL}", json=data)
    
    if response.status_code == 200:
        click.echo("Tarefa alterada com sucesso!")
        click.echo("Response: " + str(response.json()))
    elif response.status_code == 404:
        click.echo("Erro: Tarefa não encontrada.")
    else:
        click.echo(f"Erro ao alterar a tarefa: {response.json()}")

if __name__ == "__main__":
    alterar()