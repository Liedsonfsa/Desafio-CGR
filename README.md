# Desafio CGR

O solução para o desafio foi desenvolvida utilizando Python, Flask e SQLite3.

## Estrutura do projeto
```bash
desafio-cgr/
    |
    |--- controllers/ # manipula as requisiçoes
    |       |--- analisar_gargalos.py
    |       |--- equipamentos.py
    |       |--- logs.py
    |       |--- recursos.py
    |
    |--- database/
    |       |--- conexao.py # estabelece uma nova conexão com o banco de dados
    |       |--- equipamentos.db # arquivo com os dados
    |       |--- init.py # cria as tabelas e insere os valores
    |       |--- schema.sql # schema das tabelas e comandos de inserção dos valores
    |
    |--- models/ # realiza a comunicação com o banco de dados
    |       |--- equipamentos.py 
    |       |--- logs.py
    |       |--- recursos.py
    |
    |--- service/ # cógica de serviço
    |       |--- analise.py # contém a lógica de serviço da análise de gargalos
    |       |--- notificacoes.py # contém a lógica de serviço das notificações no terminal
    |
    |--- .gitignore
    |--- app.py
    |--- README.md
    |--- requirements.txt

```

## Clonando e acessando o repositório
```bash
git clone https://github.com/Liedsonfsa/Desafio-CGR.git
cd Desafio-CGR
```

## Criando um ambiente virtual

### No linux

#### Criando ambiente
Digite no seu terminal:
```bash
python -m venv venv 
```

#### Ative o ambiente
Digite no seu terminal:
```bash
source venv/bin/activate
```

### No Windows

#### Criando ambiente

##### Pelo CMD
Digite no seu terminal:
```bash
venv\Scripts\Activate
```

##### Pelo PowerShell
Digite no seu terminal:
```bash
venv\Scripts\Activate.ps1
```

## Instalando as dependências
Digite no seu terminal:
```bash
pip install -r requirements.txt
```

## Executando a API
Digite no seu terminal:
```bash
python app.py
```

## 🔌 Endpoints Implementados
- ✅ `GET /equipamentos`
- ✅ `GET /equipamentos/{id}`
- ✅ `PUT /equipamentos/{id}/status`
- ✅ `GET /equipamentos/{id}/recursos`
- ✅ `POST /recursos/alocar`
- ✅ `POST /recursos/desalocar`
- ✅ `POST /recursos/melhor-recurso`
- ✅ `GET /logs`
- ✅ `POST /equipamentos/{id}/simular-falha`
- ✅ `GET /analisar-gargalos/{id}`

## Descrição dos endpoints

### `GET /equipamentos`

Esse endpoint retorna todos os equipamentos que tem no banco de dados.

#### Respostas

##### 200 - Sucesso

```json
{
  "data": [
    {
      "id": 1,
      "ip_gerenciamento": "192.168.1.1",
      "localizacao": "Rack 1 - Andar 1",
      "nome": "Servidor Principal",
      "status": "Ativo",
      "tipo": "Servidor"
    }
  ],
  "success": true
}
```

##### 404 - Não Encontrado

```json
{
  "error": "Equipamento não encontrado"
}
```

##### 500 - Erro Interno do Servidor

```json
{
  "error": "Erro interno ao buscar equipamentos"
}
```

### `GET /equipamentos/{id}`

Esse endpoint retorna o equipamento que possui um determinado id.

#### Respostas

##### 200 - Sucesso

```json
{
  "data": {
    "id": 1,
    "nome": "Servidor Principal",
    "status": "Online"
  },
  "message": "Equipamento encontrado",
  "success": true
}
```

##### 404 - Não Encontrado

```json
{
    "error": "Equipamento não encontrado"
}
```

##### 500 - Erro Interno no Servidor

```json
{
    "error": "Erro interno ao buscar equipamento"
}
```

### `PUT /equipamentos/{id}/status`

Esse endpoint atualiza o status de um equipamento que possui um determinado id.

#### Requisição
A requisição irá conter o novo status e a descrição que será utilizada como mensagem no log.
```json
{
  "descricao": "Equipamento enviado para manutenção",
  "status": "Manutenção"
}
```

#### Respostas

##### 200 - Sucesso

```json
{
  "descricao": "Equipamento enviado para manutenção",
  "equipamento_id": 1,
  "novo_status": "Manutenção",
  "tipo_evento": "Status Change"
}
```

##### 400 - Requisição mal feita
Quando algum dado ou campo da requisição está errado.
```json
{
  "error": "Dados incompletos ou incorretos no request"
}
```

##### 500 - Erro Interno no Servidor
Quando a falha ocorre na função de atualizar do models.
```json
{
  "error": "Falha ao atualizar status"
}
```

ou:


Quando a falha ocorre no controllers.
```json
{
  "error": "Erro interno ao alterar status"
}
```

### `GET /equipamentos/{id}/recursos`

Esse endpoint retorna todos os recursos de um equipamento com um determinado id.

#### Respostas

##### 200 - Sucesso

```json
{
  "equipamento_id": 1,
  "recursos": [
    {
      "id": 1,
      "nome": "Porta Ethernet",
      "status": "Disponível"
    }
  ],
  "sucesso": true
}
```

##### 404 - Não Encontrado

```json
{
  "error": "Nenhum recurso encontrado para este equipamento",
  "sucesso": false
}
```

##### 500 - Erro Interno no Servidor

```json
{
  "error": "Erro interno ao buscar recursos",
  "sucesso": false
}
```
### `POST /recursos/alocar`

Esse endpoint faz a locação de um recurso, com base no seu tipo e id do equipamento.

#### Requisição
A requisição irá conter o id do equipamento e tipo do recurso que deve ser alocado.
```json
{
  "equipamento_id": 1,
  "tipo_recurso": "Porta Ethernet"
}
```

#### Respostas

##### 200 - Sucesso

```json
{
  "sucesso": "recurso alocado com sucesso"
}
```

##### 400 - Requisição mal feita

```json
{
  "error": "Dados incompletos ou errados no request",
  "sucesso": false
}
```

##### 409 - Recurso não Disponível

```json
{
  "error": "Recurso não disponível para alocação",
  "sucesso": false
}
```

##### 500 - Erro Interno no Servidor

```json
{
  "error": "Erro interno ao alocar recurso",
  "sucesso": false
}
```

### `POST /recursos/desalocar`

Esse endpoint faz a desalocação de um recurso, com base no seu id.

#### Respostas

##### 200 - Sucesso

```json
{
  "message": "Recurso desalocado com sucesso",
  "recurso_id": 1,
  "sucesso": true
}
```

##### 400 - Requisição mal feita

```json
{
  "error": "ID do recurso não fornecido",
  "sucesso": false
}
```

##### 500 - Erro Interno no Servidor

```json
{
  "error": "Erro interno ao desalocar recurso",
  "sucesso": false
}
```

### `POST /recursos/melhor-recurso`

#### Requisição

```json
{
  "equipamento_id": 1,
  "tipo_recurso": "Porta Ethernet"
}
```

#### Respostas

##### 200 - Sucesso

```json
{
  "equipamento_id": 1,
  "message": "Recurso encontrado",
  "recurso_id": 1,
  "success": true,
  "tipo_recurso": "Porta Ethernet",
  "valor_recurso": "Eth0/1"
}
```

##### 400 - Requisição mal feita

```json
{
  "error": "Tipo de recurso não especificado",
  "sucesso": false
}
```

##### 404 - Não Encontrado

```json
{
  "message": "Nenhum recurso disponível encontrado",
  "success": false
}
```

##### 500 - Erro Interno no Servidor

```json
{
  "error": "Erro interno na alocação inteligente",
  "sucesso": false
}
```

### `GET /logs`

Esse endpoint retorna todos os logs registtrados no banco de dados.

##### 200 - Sucesso

```json
{
  "data": [
    {
      "data_hora": "2023-05-20 14:30:00",
      "descricao": "Equipamento atualizado",
      "equipamento_id": 5,
      "id": 1,
      "tipo_evento": "Status Change"
    }
  ],
  "message": "Logs recuperados com sucesso",
  "success": true
}
```

##### 404 - Não Encontrado

```json
{
  "sucesso": False,
  "message": "Nenhum log encontrado",
  "logs": []
}
```
##### 500 - Erro Interno no Servidor

```json
{
  "sucesso": False,
  "message": "Erro interno ao buscar logs"
}
```

### `POST /equipamentos/{id}/simular-falha`

Esse endpoint possibilita a simulação de  falhas aleatórias em aproximadamente 30% dos recursos de um equipamento

##### 200 - Sucesso

```json
{
  "equipamento_id": 1,
  "message": "Simulação de falha concluída. 3 recursos afetados.",
  "recursos_afetados": 3,
  "success": true
}
```

##### 404 - Não Encontrado

```json
{
  "message": "Nenhum recurso encontrado para o equipamento",
  "success": false
}
```
##### 500 - Erro Interno no Servidor

```json
{
  "message": "Erro durante a simulação de falha",
  "success": false
}
```
### `GET /analisar-gargalos/{id}`

Esse endpoint realiza a análise de gargalos de um determinado equipamento.

### Respostas

##### 200 - Sucesso

```json
{
  "alerta": "CRÍTICO: Mais de 30% dos recursos com problemas",
  "equipamento_id": 1,
  "lista_problemas": [
    {
      "dias_sem_atualizacao": 2,
      "recurso_id": 5,
      "status": "Indisponível",
      "tipo_recurso": "Porta Ethernet",
      "ultima_atualizacao": "2023-05-20 14:30:00",
      "valor_recurso": "Eth0/2"
    }
  ],
  "nome_equipamento": "Switch Principal",
  "porcentagem_problemas": "30.00%",
  "recursos_problematicos": 3,
  "timestamp_analise": "2023-05-22 10:15:00",
  "total_recursos": 10
}
```

##### 404 - Não Encontrado

```json
{
  "equipamento_id": 999,
  "erro": "Equipamento não encontrado",
  "timestamp_analise": "2023-05-22 10:15:00"
}
```

##### 500 - Erro Interno no Servidor

```json
{
  "equipamento_id": 1,
  "erro": "Erro inesperado: could not connect to database",
  "timestamp_analise": "2023-05-22 10:15:00"
}
```

## Lógica aplicada para simular falhas

## Lógica aplicada para analisar gargalos

O endpoint de alálise de gargalos identifica recursos problemáticos em um equipamento específico e calcula métricas de saúde. As métricas que são levadas em consideração durante a análise são as seguintes:
- Total de recursos
- Recursos com problemas
- Porcentagem de problemas
- Lista detalhada de recursos problemáticos

Caso o número de recursos com problemas seja > 30%, a resposta da requisição irá conter um campo chamado alerta contendo essa informação.

#### servie/analise.py

Como a lógica da análise está contida nesse arquivo.

É feita uma consulta para obter o nome do equipamento com base no seu id:
```python
cursor.execute("SELECT nome FROM EquipamentosRede WHERE id = ?", (equipamento_id,))
equipamento = cursor.fetchone()
```

Caso o equipamento nã exista, será retornada essa informação sendo tida como um erro na nossa resposta.
```python
if not equipamento:
    resultado['erro'] = "Equipamento não encontrado"
    return resultado

# se o equipamento existir, o nome dele será adicionado na resposta.
resultado['nome_equipamento'] = equipamento[0]
```

Logo após, é realizada a contagem da quantidade total de recursos associados a esse equipamento utilizando a função COUNT do SQLite:
```python
cursor.execute("""
SELECT COUNT(*) 
FROM RecursosRede 
WHERE equipamento_id = ?
""", (equipamento_id,))
resultado['total_recursos'] = cursor.fetchone()[0]
```

Depois, é realizada um consulta que irá selecionar os campos: id, tipo_recurso, valor_recurso, status_alocacao e ultima_atualizacao, de todos os recursos que possuem o status de alocação com os valores Indisponível ou Com Problema. Em seguida, armazena a quantidade de recursos problemáticos na resposta.
```python
cursor.execute("""
SELECT id, tipo_recurso, valor_recurso, status_alocacao, ultima_atualizacao
FROM RecursosRede
WHERE equipamento_id = ?
  AND status_alocacao IN ('Indisponível', 'Com Problema')
ORDER BY ultima_atualizacao DESC
""", (equipamento_id,))
recursos_problematicos = cursor.fetchall()
resultado['recursos_problematicos'] = len(recursos_problematicos)
```

Esse trecho, realiza o cálculo para saber qual a porcentagem dos recursos problemáticos: 
```python
if resultado['total_recursos'] > 0:
  porcentagem = (resultado['recursos_problematicos'] / resultado['total_recursos']) * 100
  resultado['porcentagem_problemas'] = f"{porcentagem:.2f}%"
  
  # alerta de porcentagem crítica
  if porcentagem > 30:
      resultado['alerta'] = "CRÍTICO: Mais de 30% dos recursos com problemas"
```

Por fim, são adicionados na resposta, as informações sobre os recursos e também a quantidade de dias que ele está sem atualização.
```python
for recurso in recursos_problematicos:
  id_recurso, tipo, valor, status, ultima_atualizacao = recurso
  
  dias_sem_atualizacao = (datetime.now() - datetime.strptime(ultima_atualizacao, "%Y-%m-%d %H:%M:%S")).days
  
  resultado['lista_problemas'].append({
      'recurso_id': id_recurso,
      'tipo_recurso': tipo,
      'valor_recurso': valor,
      'status': status,
      'ultima_atualizacao': ultima_atualizacao,
      'dias_sem_atualizacao': dias_sem_atualizacao
  })

return resultado
```
