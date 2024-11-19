import click
import requests
import os

@click.command()
@click.option('--incompletas', is_flag=True, help="Se especificado, lista apenas as tarefas incompletas. Caso contrário, lista todas as tarefas.")
def listar(incompletas):
    params = {'status': 'incompletas'} if incompletas else {}
    api_url = os.getenv('API_URL')
    cert_path = os.getenv('CERT_PATH')
    api_key = os.getenv("API_KEY")
    headers = {"X-API-KEY": api_key}
    
    try:
        response = requests.get(
            api_url,
            headers=headers,
            verify=cert_path,
            params=params
        )
    
        if response.status_code == 200:
            tarefas = response.json()
            if tarefas:
                for tarefa in tarefas:
                    click.echo(f"UUID: {tarefa['uuid']}, Título: {tarefa['titulo']}, Concluída: {tarefa['concluida']}")
            else:
                click.echo("Nenhuma tarefa encontrada.")
        else:
            click.echo(f"Erro ao listar tarefas: {response.json()}")
            
    except requests.exceptions.SSLError as e:
        print(f"Erro SSL: {e}")
    except Exception as e:
        print(f"Erro: {e}")
            
if __name__ == "__main__":
    listar()