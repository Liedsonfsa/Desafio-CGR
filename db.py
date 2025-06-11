import sqlite3 as sql

conn = sql.connect('equipamentos.db')

cursor = conn.cursor()

query = '''
CREATE TABLE EquipamentosRede (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    ip_gerenciamento TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'Online',
    localizacao TEXT NOT NULL
);
'''

cursor.execute(query)

conn.commit()

query = '''
CREATE TABLE RecursosRede (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    tipo_recurso TEXT NOT NULL,
    valor_recurso TEXT NOT NULL,
    status_alocacao TEXT NOT NULL DEFAULT 'Disponível',
    cliente_associado TEXT,
    ultima_atualizacao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equipamento_id) REFERENCES EquipamentosRede(id) ON DELETE CASCADE
);
'''

cursor.execute(query)

conn.commit()

query = '''
CREATE TABLE EventosLogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_evento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    FOREIGN KEY (equipamento_id) REFERENCES EquipamentosRede(id) ON DELETE CASCADE
);
'''

cursor.execute(query)

conn.commit()
