import duckdb

# Conecta ao banco de dados
con = duckdb.connect("pi2_solucao_hospitalar.db")

# Cria todas as tabelas necessárias, considerando restrições de unicidade e chaves estrangeiras
con.sql("""
            CREATE TABLE IF NOT EXISTS paciente (
                id STRING PRIMARY KEY,
                nome STRING,
                cpf STRING UNIQUE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS insumos (
            id STRING PRIMARY KEY,
            nome STRING UNIQUE,
            durabilidade INTEGER
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS tipoequipamento (
            id STRING PRIMARY KEY,
            nome STRING UNIQUE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS especialidade (
                id STRING PRIMARY KEY,
                nome STRING UNIQUE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS sala (
            id STRING PRIMARY KEY,
            numero STRING UNIQUE,
            setor STRING,
            capacidade STRING,
            caracteristica STRING
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS equipamento (
                id STRING PRIMARY KEY,
                marca STRING,
                modelo STRING,
                patrimonio STRING UNIQUE,
                intervalomanutencao INTEGER,
                id_tipoequipamento STRING REFERENCES tipoequipamento(id),
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS reposicaoinsumos (
            id STRING PRIMARY KEY,
            id_equipamento STRING REFERENCES equipamento(id),
            id_insumo STRING REFERENCES insumos(id),
            data DATE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS medico (
                id STRING PRIMARY KEY,
                nome STRING,
                id_especialidade STRING REFERENCES especialidade(id),
                numeroCRM STRING UNIQUE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS internacao (
                id STRING PRIMARY KEY,
                id_paciente STRING REFERENCES paciente(id),
                id_sala STRING REFERENCES sala(id),
                id_medico STRING REFERENCES medico(id),
                data DATE
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS manutencao (
            id STRING PRIMARY KEY,
            data DATE,
            id_equipamento STRING REFERENCES equipamento(id)
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS tratamento (
            id STRING PRIMARY KEY,
            nome STRING UNIQUE,
            descricao STRING,
            restricoes STRING,
            id_tipoequipamento STRING REFERENCES tipoequipamento(id)
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS setorporta (
            id STRING PRIMARY KEY,
            marca STRING,
            modelo STRING,
            sala_id STRING REFERENCES sala(id)
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS localizacaoequipamento (
            id STRING PRIMARY KEY,
            data DATE,
            id_sala STRING REFERENCES sala(id),
            id_equipamento STRING REFERENCES equipamento(id)
            );
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS prontuario (
            id STRING PRIMARY KEY,
            id_paciente STRING REFERENCES paciente(id),
            id_sala STRING REFERENCES sala(id),
            id_tratamento STRING REFERENCES tratamento(id),
            id_medico STRING REFERENCES medico(id),
            data DATE,
            observacoes STRING
            ); 
        """)

con.sql("""
            CREATE TABLE IF NOT EXISTS equipamentoativo (
            id STRING PRIMARY KEY,
            id_equipamento STRING UNIQUE REFERENCES equipamento(id),
            data DATE
            );
        """)