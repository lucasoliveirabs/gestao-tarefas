import os
import requests
import click

@click.command()
@click.option('--titulo', required=True, help='Título da tarefa')
@click.option('--descricao', required=True, help='Descrição da tarefa')
def criar(titulo, descricao):
    data = {"titulo": titulo, "descricao": descricao}
    api_url = os.getenv('API_URL')
    cert_path = os.getenv('CERT_PATH')
    api_key = os.getenv("API_KEY")
    headers = {"X-API-KEY": api_key}

    try:
        response = requests.post(
            api_url,
            headers=headers,
            json=data,
            verify=cert_path
        )
        
        if response.status_code == 201:
            click.echo("Tarefa criada com sucesso!")
        else:
            click.echo(f"Erro ao criar tarefa: {response.json()}")
            
    except requests.exceptions.SSLError as e:
        print(f"Erro SSL: {e}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == '__main__':
    criar()