import duckdb

# Conecta ao banco de dados
con = duckdb.connect("pi2_solucao_hospitalar.db")

con.sql("""
            DROP TABLE prontuario;
            DROP TABLE equipamentoativo;
            DROP TABLE manutencao;
            DROP TABLE reposicaoinsumos;
            DROP TABLE localizacaoequipamento;
            DROP TABLE equipamento;
            DROP TABLE internacao;
            DROP TABLE setorporta;
            DROP TABLE medico;
            DROP TABLE especialidade;
            DROP TABLE sala;
            DROP TABLE paciente;
            DROP TABLE tratamento;
            DROP TABLE insumos;
            DROP TABLE tipoequipamento;
        """)