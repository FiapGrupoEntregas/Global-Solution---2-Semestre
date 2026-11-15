-- Modelo relacional do TriaSUS (POC, dados sintéticos)
DROP TABLE IF EXISTS solicitacao;
DROP TABLE IF EXISTS regiao;

CREATE TABLE regiao (
    id_regiao      INTEGER PRIMARY KEY,
    nome           TEXT NOT NULL UNIQUE,
    ajuste_fila    REAL NOT NULL            -- pontos somados ao escore (regra pública)
);

CREATE TABLE solicitacao (
    id_solicitacao       INTEGER PRIMARY KEY,
    idade                INTEGER NOT NULL CHECK (idade BETWEEN 0 AND 120),
    sexo                 TEXT NOT NULL CHECK (sexo IN ('F','M')),
    id_regiao            INTEGER NOT NULL REFERENCES regiao(id_regiao),
    porte                TEXT NOT NULL CHECK (porte IN ('pequeno','medio','grande')),
    especialidade        TEXT NOT NULL,
    n_sinais_alerta      INTEGER NOT NULL,
    comorbidades         INTEGER NOT NULL,
    dias_espera          INTEGER NOT NULL CHECK (dias_espera >= 0),
    prioridade_real      INTEGER NOT NULL CHECK (prioridade_real BETWEEN 0 AND 3),
    prioridade_prevista  INTEGER NOT NULL CHECK (prioridade_prevista BETWEEN 0 AND 3),
    texto_livre          TEXT
);
CREATE INDEX idx_sol_prio ON solicitacao(prioridade_prevista, dias_espera);
CREATE INDEX idx_sol_regiao ON solicitacao(id_regiao);
