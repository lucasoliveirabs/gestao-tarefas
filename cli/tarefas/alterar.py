import click
import requests
import os

@click.command()
@click.option('--uuid', prompt='UUID da tarefa', help='UUID da tarefa a ser alterada.')
@click.option('--titulo', help='Novo título da tarefa.')
@click.option('--descricao', help='Nova descrição da tarefa.')
@click.option('--concluida', type=bool, help='Define se a tarefa está concluída. Booleano (True ou False).')
def alterar(uuid, titulo, descricao, concluida):
    data = {}
    api_url = os.getenv('API_URL')
    url = f"{api_url}/{uuid}"
    cert_path = os.getenv('CERT_PATH')
    api_key = os.getenv("API_KEY")
    headers = {"X-API-KEY": api_key}

    if titulo:
        data["titulo"] = titulo
    if descricao:
        data["descricao"] = descricao
    if concluida is not None:
        data["concluida"] = concluida
            
    try: 
        response = requests.patch(
            url,
            headers=headers,
            json=data,
            verify=cert_path
        )
    
        if response.status_code == 200:
            click.echo("Tarefa alterada com sucesso!")
        elif response.status_code == 404:
            click.echo("Erro: Tarefa não encontrada.")
        else:
            click.echo(f"Erro ao alterar a tarefa: {response.json()}")
            
    except requests.exceptions.SSLError as e:
        print(f"Erro SSL: {e}")
    except Exception as e:
        print(f"Erro: {e}")
        
        
if __name__ == "__main__":
    alterar()