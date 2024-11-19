# `gestao-tarefas`

O projeto consiste em uma solução simples pensada para uso local para gestão de tarefas, semelhante a uma TODO list. O projeto é composto por três componentes principais, cada um configurado para execução em container dedicado:

- **Banco de dados relacional** [PostgreSQL](https://www.postgresql.org/)
- **API REST** construída em [Flask](https://flask.palletsprojects.com/en/stable/), responsável por fornecer endpoints para manipulação das tarefas. Após deploy, consulte a [documentação](https://localhost:443/swagger/)
- **Cliente CLI** desenvolvido com [Click](https://click.palletsprojects.com/en/stable/).

## Configuração do Ambiente de Desenvolvimento

### Pré-requisitos:

Confirme em sua máquina a instalação de: [Python3](https://www.python.org/downloads/), [Docker](https://www.docker.com/get-started/) e [Docker Compose](https://docs.docker.com/compose/install/). Confirme também que o Docker Daemon está ativo:

```bash
python3 --version
docker --version
docker-compose --version
docker info
```

### Passo a passo:

1. **Execute o script `start_project.sh`** para configurar e iniciar o projeto:

   ```bash
   chmod +x start_project.sh
   ./start_project.sh
   ```

2. **Inicie o container CLI sob demanda** para interagir com a API:

   ```bash
   chmod +x start_cli.sh
   ./start_cli.sh
   python3 cli.py
   ```

3. **Acesse o diretório 'tarefas' para acessar os scripts**. Use o argumento "--help" sempre que desejar obter informações sobre um comando:

   ```bash
   cd tarefas/
   python3 criar.py --titulo "Primeira tarefa" --descricao "Testar em ambiente de desenvolvimento"
   python3 listar.py --incompletas
   python3 alterar.py --uuid xxx --concluida true
   python3 excluir.py --help
   ```

4. **Para encerrar os containers:**

   ```bash
   docker-compose down
   ```

---

#### Observações técnicas:

O arquivo docker-compose.yaml foi projetado para executar os serviços, os testes unitários da API e realizar o deploy via Docker.

A solução conteinerizada foi projetada considerando o contexto de um ambiente de desenvolvimento local mas com a flexibilidade necessária para integração futura em pipelines CI/CD corporativos, focando em requisitos de segurança e escalabilidade. Nesse caso, recomendamos incluir a implementação de testes de integração, de penetração (OWASP zap)[https://www.zaproxy.org/docs/] e a construção de uma pipeline CI/CD (Jenkins)[https://www.jenkins.io/].

- **Segurança**:

  - SSL: Atualmente a API utiliza certificados autoassinados gerados com [OpenSSL](https://docs.openssl.org/master/), garantindo conexão segura entre CLI e API em ambiente containerizado. Configuramos o certificado cliente para considerar 127.0.0.1, localhost e `web` como Subject Alternative Names (SANs), garantindo compatibilidade e exclusiva entre containers `cli` e `web`.
    Com expansão de componentes, para ambientes além do desenvolvimento ou para situações que precisem de integração com DNS externoa, recomendamos o uso de certificados emitidos por Autoridades Certificadoras. Considerando a construção de uma pipeline CI/CD, sugerimos os certificados [gerenciados em nuvem](https://aws.amazon.com/pt/certificate-manager/);
  - CORS: Atualmente, se tratando de uma solução interna e com conexão CLI-API já tratada via certificado SSL, CORS não se faz estritamente necessário.
    Com expansão de componentes, para ambientes além do desenvolvimento ou sobretudo casos que precisem de integração com origens externas e conexão com internet, recomendamos atualização da configuração do [CORS](https://flask-cors.readthedocs.io/en/v1.1/);
  - API Key: Novamente considerando o contexto da solução, no momento a adoção de API Keys para melhoria de segurança e controle de acesso aos endpoints se faz suficiente. Exportamos as variáveis de ambiente no script de inicialização `start_project.sh` e habilitamos acesso CLI-API, reforçando segurança SSL.
    JWT e Oauth2 se mostram opções importantes na expansão e/ou abertura à outros componentes internos ou externos. Nesse caso é interessante configurar as variáveis na pipeline;
  - [Flask-RESTx](https://flask-restx.readthedocs.io/en/latest/): Extensão adotada na construção da API RESTful. Ao priorizar segurança e documentação, fornece serialização automatizada, decorators para definição de autenticação por endpoint ou por namespace, swagger integrado, validação de inputs e tratamento automático de erros em função de model específico por endpoint;

- **Migração do Banco de Dados**: O projeto usa `Flask-Migrate` para gerenciar mudanças no esquema do banco de dados. Sempre que fizer alterações nos modelos, vá ao ambiente containerizado e em `app/api/` execute `flask db migrate` para gerar as migrações necessárias. As mudanças são aplicadas a cada interação CLI via `flask db upgrade`. Os dados serão persistidos conforme o [volume](https://docs.docker.com/engine/storage/volumes/) definido no docker-compose;

- **CLI sob Demanda**: O container `cli` é executado sob demanda, otimizando recursos. A inicialização do shell interativo se dá na execução de `start_cli.sh`;

- **Dependências**: Todas as dependências necessárias estão contidas nos containers Docker. Não se faz necessário configurar um ambiente Python local;

- **Variáveis de ambiente**: Todas as variáveis de ambiente necessárias estão contidas no arquivo docker-compose.yml. Não se faz necessário configurar `.env`

#### Sugestão pessoal:

Considerando as exigências do setor de healthcare privado, como segurança, confiabilidade e conformidade regulatória, soluções baseadas em blockchain permissionada podem ser exploradas como um diferencial estratégico para expansão futura. Essa abordagem permitiria:

- Imutabilidade e Rastreabilidade: Garantir que alterações e históricos sejam permanentemente registrados e auditáveis;
- Confiança Compartilhada: Facilitar a colaboração entre departamentos, unidades e/ou stakeholders por meio de um sistema transparente e seguro;
- Compliance: Implementação e atendimento de requisitos regulatórios em uma infraestrutura confiável

Embora o foco atual seja a gestão interna eficiente de tarefas, soluções como [Hyperledger Fabric](https://hyperledger-fabric.readthedocs.io/en/release-2.5/) podem ser avaliadas para cenários mais complexos, como auditoria de tarefas críticas ou integração entre múltiplas partes interessadas.

---

Fique à vontade para entrar em contato! Obrigado e bom proveito!
