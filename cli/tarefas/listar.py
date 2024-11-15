import click
import requests
import os

@click.command()
@click.option('--incompletas', is_flag=True, help="Se especificado, lista apenas as tarefas incompletas. Caso contrário, lista todas as tarefas.")
def listar(incompletas):
    """Lista as tarefas da API. Se a opção 'incompletas' for especificada, retorna apenas as tarefas incompletas. Caso contrário, retorna todas as tarefas."""
    params = {'status': 'incompletas'} if incompletas else {}
    response = requests.get(os.getenv('API_URL'), params=params)
    
    if response.status_code == 200:
        tarefas = response.json()
        if tarefas:
            for tarefa in tarefas:
                click.echo(f"ID: {tarefa['id']}, Título: {tarefa['titulo']}, Concluída: {tarefa['concluida']}")
        else:
            click.echo("Nenhuma tarefa encontrada.")
    else:
        click.echo(f"Erro ao listar tarefas: {response.json()}")
        
if __name__ == "__main__":
    listar()