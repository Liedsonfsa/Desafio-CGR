# Desafio CGR

O solução para o desafio foi desenvolvida utilizando Python, Flask e SQLite3.

## Arquitetura do projeto

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
```bash
source venv/bin/activate
```

### No Windows

#### Pelo CMD
```bash
venv\Scripts\Activate
```

#### Pelo PowerShell
```bash
venv\Scripts\Activate.ps1
```

## Instalando as dependências
```bash
pip install -r requirements.txt
```

## Executando a API
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
- ✅ `GET /logs`
- ✅ `POST /equipamentos/{id}/simular-falha`
- ✅ `GET /analisar-gargalos/{id}`

## Descrição breve dos endpoints

## Descrição da lógica para simular falhas

## Descrição da lógica para analisar gargalos