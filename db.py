import sqlite3 as sql

conn = sql.connect('equipamentos.db')

cursor = conn.cursor()

query = '''INSERT INTO Equipamentos (nome, tipo, ip_gerenciamento, status, localizacao) VALUES
('Switch Principal - Andar 1', 'Switch', '192.168.1.1', 'Online', 'Data Center - Rack 1'),
('Router Corporativo', 'Router', '192.168.1.254', 'Online', 'Data Center - Rack 2'),
('Servidor Web', 'Server', '192.168.2.100', 'Manutenção', 'Data Center - Rack 3'),
('Firewall Perimeter', 'Firewall', '192.168.1.2', 'Online', 'Data Center - Rack 1'),
('AP WiFi - Recepção', 'Access Point', '192.168.3.10', 'Online', 'Recepção - Teto');'''

cursor.execute(query)

conn.commit()
