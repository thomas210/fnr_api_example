# API Python — demonstração de IaaS e PaaS

API sem banco de dados para publicar a mesma aplicação em uma instância AWS e no Render. O código é o mesmo; o objetivo é comparar as responsabilidades operacionais.

## Endpoints

| Método | Endpoint | Objetivo |
|---|---|---|
| GET | `/` | Apresenta a API e lista os endpoints. |
| GET | `/health` | Verificação de saúde da aplicação. |
| GET | `/saudacao/Thomas` | Retorna uma saudação personalizada. |
| GET | `/saudacao/Thomas?idioma=en` | Demonstra parâmetro de consulta. |
| GET | `/info` | Exibe ambiente, provedor e versão configurados. |

## Execução local

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://localhost:5000`.

O arquivo `requests.http` reúne chamadas prontas para o REST Client do VS Code. Também é possível abrir as URLs no navegador.

Para demonstrar variáveis de ambiente no PowerShell:

```powershell
$env:APP_ENV="aula"
$env:CLOUD_PROVIDER="computador-local"
$env:APP_VERSION="1.0.0"
python app.py
```

## Render — exemplo de PaaS

1. Coloque a pasta em um repositório Git.
2. No Render, crie um **Blueprint** usando o arquivo `render.yaml` ou um **Web Service**.
3. Se optar pelo Web Service, configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
4. Após o deploy, abra `/health` e `/info` na URL fornecida.

Ponto para destacar: a equipe envia o código e informa como construir/iniciar. A plataforma prepara o runtime, executa o processo, fornece URL e realiza verificações de saúde.

## AWS EC2 — exemplo de IaaS

Use uma instância Linux apenas para demonstração. Libere no grupo de segurança somente SSH para o seu IP e a porta HTTP utilizada na aula.

Fluxo conceitual dentro da instância:

```bash
sudo apt update
sudo apt install -y python3-venv git
git clone URL_DO_REPOSITORIO
cd api-python-iaas-paas
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export APP_ENV=producao
export CLOUD_PROVIDER=aws-ec2-iaas
export APP_VERSION=1.0.0
gunicorn --bind 0.0.0.0:8000 app:app
```

Para uma aula rápida, acesse `http://IP_PUBLICO:8000/health`. Em produção real, o processo deveria ser gerenciado por um serviço do sistema e colocado atrás de um servidor HTTP/reverse proxy, com HTTPS e regras de rede mais restritas.

Ponto para destacar: na EC2 a equipe escolhe e configura a máquina, sistema operacional, pacotes, processo, rede, atualizações e monitoramento.

## Comparação para apresentar

| Decisão/tarefa | Render (PaaS) | AWS EC2 (IaaS) |
|---|---|---|
| Preparar sistema operacional | Plataforma | Equipe |
| Instalar Python e componentes do SO | Plataforma | Equipe |
| Instalar dependências da aplicação | Comando de build | Equipe executa/configura |
| Manter o processo ativo | Plataforma | Equipe |
| Configurar acesso de rede | Simplificado pela plataforma | Equipe/grupo de segurança |
| Entregar código e variáveis | Equipe | Equipe |
| Corrigir erros da aplicação | Equipe | Equipe |

## Documentação oficial consultada

- [Implantação de uma aplicação Flask no Render](https://render.com/docs/deploy-flask)
- [Referência do arquivo Blueprint `render.yaml`](https://render.com/docs/blueprint-spec)
- [Grupos de segurança do Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-security-group.html)
