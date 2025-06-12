CREATE TABLE EquipamentosRede (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    ip_gerenciamento TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'Online',
    localizacao TEXT NOT NULL
);

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

CREATE TABLE EventosLogs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    equipamento_id INTEGER NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_evento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    FOREIGN KEY (equipamento_id) REFERENCES EquipamentosRede(id) ON DELETE CASCADE
);

INSERT INTO EquipamentosRede (nome, tipo, ip_gerenciamento, status, localizacao) VALUES
('Switch Principal', 'Switch', '192.168.1.1', 'Online', 'Rack 1 - Andar 1'),
('Router Borda', 'Router', '192.168.1.2', 'Online', 'Rack 1 - Andar 1'),
('Servidor Web', 'Server', '192.168.1.10', 'Online', 'Rack 2 - Andar 1');

INSERT INTO recursos (equipamento_id, tipo_recurso, valor_recurso, status_alocacao, cliente_associado) VALUES
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

INSERT INTO logs (equipamento_id, tipo_evento, descricao) VALUES
(1, 'Status Change', 'Equipamento inicializado'),
(2, 'Resource Allocated', 'IP 192.168.2.2 alocado para Cliente C'),
(3, 'Resource Allocated', 'Porta Eth1 alocada para Cliente D'),
(1, 'Resource Allocated', 'Porta Eth0/3 alocada para Cliente A'),
(1, 'Resource Reserved', 'Porta Eth0/4 reservada para Cliente B'),
(3, 'Resource Reserved', 'IP 192.168.3.10 reservado para Cliente E');
