import sqlite3 as sql
from database.conexao import conectar

conn = conectar()

cursor = conn.cursor()

query = '''
INSERT INTO EquipamentosRede (nome, tipo, ip_gerenciamento, status, localizacao) VALUES
('Switch Principal', 'Switch', '192.168.1.1', 'Online', 'Rack 1 - Andar 1'),
('Router Borda', 'Router', '192.168.1.2', 'Online', 'Rack 1 - Andar 1'),
('Servidor Web', 'Server', '192.168.1.10', 'Online', 'Rack 2 - Andar 1');
'''

cursor.execute(query)

conn.commit()

query = '''
INSERT INTO RecursosRede (equipamento_id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado) VALUES
(1, 'Porta Ethernet', 'Eth0/1', 'Disponível', NULL),
(1, 'Porta Ethernet', 'Eth0/2', 'Disponível', NULL),
(1, 'Porta Ethernet', 'Eth0/3', 'Alocado', 'Cliente A'),
(1, 'Porta Ethernet', 'Eth0/4', 'Reservado', 'Cliente B'),
(1, 'Porta Ethernet', 'Eth0/5', 'Disponível', NULL),
(2, 'IP v4', '192.168.2.1', 'Disponível', NULL),
(2, 'IP v4', '192.168.2.2', 'Alocado', 'Cliente C'),
(2, 'IP v6', '2001:db8::1', 'Disponível', NULL),
(2, 'IP v6', '2001:db8::2', 'Disponível', NULL),
(3, 'Porta Ethernet', 'Eth1', 'Alocado', 'Cliente D'),
(3, 'Porta Ethernet', 'Eth2', 'Disponível', NULL),
(3, 'IP v4', '192.168.3.10', 'Reservado', 'Cliente E');
'''

cursor.execute(query)

conn.commit()

query = '''
INSERT INTO EventosLogs (equipamento_id, tipo_evento, descricao) VALUES
(1, 'Status Change', 'Equipamento inicializado'),
(2, 'Resource Allocated', 'IP 192.168.2.2 alocado para Cliente C'),
(3, 'Resource Allocated', 'Porta Eth1 alocada para Cliente D'),
(1, 'Resource Allocated', 'Porta Eth0/3 alocada para Cliente A'),
(1, 'Resource Reserved', 'Porta Eth0/4 reservada para Cliente B'),
(3, 'Resource Reserved', 'IP 192.168.3.10 reservado para Cliente E');
'''

cursor.execute(query)

conn.commit()
