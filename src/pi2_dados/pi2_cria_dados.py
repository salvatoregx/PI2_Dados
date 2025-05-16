import duckdb
import pandas as pd
from datetime import date
from faker import Faker
import random
import os

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTAS_DIR = os.path.join(BASE_DIR, 'listas')

# Conecta ao banco de dados
con = duckdb.connect("pi2_solucao_hospitalar.db")

# Cria dados fictícios para cada campo, permitindo simular análises e visualizações
# paciente (id, nome, cpf)
n_pacientes = 1000

data = [
    (
        i + 1,
        fake.name(),
        fake.unique.random_int(11111111111, 99999999999)
    )
    for i in range (n_pacientes)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO paciente SELECT * FROM data
        """)

# insumos (id, nome, durabilidade)
with open(os.path.join(LISTAS_DIR, 'insumos.txt'), 'r') as file:
    insumos = [line.strip() for line in file]
n_insumos = len(insumos)

data = [
    (
        i + 1,
        insumos[i],
        random.randint(5, 60)
    )
    for i in range (n_insumos)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO insumos SELECT * FROM data
        """)

# tipoequipamento (id, nome)
with open(os.path.join(LISTAS_DIR, 'tipoequipamento.txt'), 'r') as file:
    tipoequipamento = [line.strip() for line in file]
n_tipoequipamento = len(tipoequipamento)

data = [
    (
        i + 1,
        tipoequipamento[i]
    )
    for i in range (n_tipoequipamento)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO tipoequipamento SELECT * FROM data
        """)

# especialidade (id, nome)
with open(os.path.join(LISTAS_DIR, 'especialidades.txt'), 'r') as file:
    especialidades = [line.strip() for line in file]
n_especialidades = len(especialidades)

data = [
    (
        i + 1,
        especialidades[i]
    )
    for i in range (n_especialidades)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO especialidade SELECT * FROM data
        """)

# sala (id, numero, setor, capacidade, caracteristica)
strings_1 = [f"1{i:02d}" for i in range(1, 11)]
strings_2 = [f"2{i:02d}" for i in range(1, 11)]
numeros_quarto = strings_1 + strings_2
n_salas = len(numeros_quarto)
setores = ["Cirurgia", "UTI", "Radiologia", "Emergência"]
capacidades = ["Single", "Duplo", "Triplo"]
caracteristicas = ["Baixa", "Média", "Alta"]

data = [
    (
        i + 1,
        numeros_quarto[i],
        random.choice(setores),
        random.choice(capacidades),
        random.choice(caracteristicas)
    )
    for i in range (n_salas)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO sala SELECT * FROM data
        """)

con.sql("""
            INSERT INTO sala VALUES ('21', '001', 'Manutenção', 'N/A', 'N/A')
        """)

# equipamento (id, marca, modelo, patrimonio, intervalomanutencao, id_tipoequipamento)
n_equipamentos = 20
marcas = ["Marca_Equipamento1", "Marca_Equipamento2"]
modelos = ["Modelo_equipamento1", "Modelo_equipamento2", "Modelo_equipamento3", "Modelo_equipamento4"]

data = [
    (
        i + 1,
        random.choice(marcas),
        random.choice(modelos),
        fake.unique.uuid4(),
        random.randint(7,30),
        random.randint(1, 5)
    )
    for i in range (n_equipamentos)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO equipamento SELECT * FROM data
        """)

# reposicaoinsumos (id, id_equipamento, id_insumo, data)
n_reposicaoinsumos = 50

data = [
    (
        i + 1,
        random.randint(1, n_equipamentos),
        random.randint(1, n_insumos),
        fake.date_between(start_date = 'today', end_date = '+10w')
    )
    for i in range (n_reposicaoinsumos)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO reposicaoinsumos SELECT * FROM data
        """)

# medico (id, nome, id_especialidade, numeroCRM)
n_medicos = 30
with open(os.path.join(LISTAS_DIR, 'siglas_estados.txt'), 'r') as file:
    estados = [line.strip() for line in file]

data = [
    (
        i + 1,
        fake.name(),
        random.randint(1, 10),
        random.choice(estados) + " " + str(random.randint(111111, 999999))
    )
    for i in range (n_medicos)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO medico SELECT * FROM data
        """)

# internacao (id, id_paciente, id_sala, id_medico, data)
n_internacoes = 20
capacidade_map = {'Single': 1, 'Duplo': 2, 'Triplo': 3}
# garantindo que o número de pacientes não ultrapasse os leitos de cada quarto
salas_df = con.sql("SELECT id, capacidade FROM sala LIMIT 20").fetchdf()
sala_capacities = {}
for _, row in salas_df.iterrows():
    sala_id = row['id']
    max_cap = capacidade_map[row['capacidade']]
    sala_capacities[sala_id] = {'max': max_cap, 'current': 0}

data = []
for i in range(n_internacoes):
    salas_disponiveis = [sala_id for sala_id in sala_capacities if sala_capacities[sala_id]['current'] < sala_capacities[sala_id]['max']]
    if not salas_disponiveis:
        break
    sala_escolhida = random.choice(salas_disponiveis)
    sala_capacities[sala_escolhida]['current'] += 1
# criando os dados de fato
    data.append((
        i + 1,
        fake.unique.random_int(1, n_pacientes),
        sala_escolhida,
        random.randint(1, n_medicos),
        fake.date_between(start_date='-8w')
    ))
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO internacao SELECT * FROM data
        """)

# manutencao (id, data, id_equipamento)
n_manutencoes = 15

data = [
    (
        i + 1,
        fake.date_between(start_date = 'today', end_date = '+8w'),
        fake.unique.random_int(1, n_equipamentos)
    )
    for i in range (n_manutencoes)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO manutencao SELECT * FROM data
        """)

# tratamento (id, nome, descricao, restricoes, id_tipoequipamento)
tratamentos = pd.read_csv(os.path.join(LISTAS_DIR, 'tratamentos.csv'))
n_tratamentos = len(tratamentos)
indice = [i+1 for i in range (n_tratamentos)]
tratamentos.insert(0, 'id', indice)

tipoequipamento_map = {tipo: idx + 1 for idx, tipo in enumerate(tipoequipamento)}

tratamentos['TipoDeEquipamento'] = (
    tratamentos['TipoDeEquipamento']
    .str.lower()
    .map(tipoequipamento_map)
)

data = pd.DataFrame(tratamentos)

con.sql("""
            INSERT INTO tratamento SELECT * FROM data
        """)

# setorporta (id, marca, modelo, sala_id)
marcas = ["Marca_Sensor1", "Marca_Sensor2"]
modelos = ["Modelo_sensor1", "Modelo_sensor2", "Modelo_sensor3", "Modelo_sensor4"]

data = [
    (
        i + 1,
        random.choice(marcas),
        random.choice(modelos),
        i + 1
    )
    for i in range (n_salas + 1)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO setorporta SELECT * FROM data
        """)

# localizacaoequipamento (id, data, id_sala, id_equipamento)
data = [
    (
        i + 1,
        fake.date_between(start_date='-1w'),
        random.randint(1, n_salas+1),
        i + 1
    )
    for i in range (n_equipamentos)
]
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO localizacaoequipamento SELECT * FROM data
        """)

# prontuario (id, id_paciente, id_sala, id_tratamento, data, observacoes)
internacoes_df = con.sql("SELECT id, id_paciente, id_sala, id_medico, data FROM internacao").fetchdf()

setor_tipo_map = {
    "Cirurgia": "cirúrgico",
    "Radiologia": "radiológico",
    "UTI": ["farmacêutico", "transfusão"],
    "Emergência": "enfermagem"
}

data = []
for idx, row in internacoes_df.iterrows():
    setor = con.sql(f"SELECT setor FROM sala WHERE id = {row['id_sala']}").fetchdf()['setor'].iloc[0]

    if setor == "Cirurgia":
        tipo = "cirúrgico"
    elif setor == "Radiologia":
        tipo = "radiológico"
    elif setor == "UTI":
        tipo = random.choice(["farmacêutico", "transfusão"])
    elif setor == "Emergência":
        tipo = "enfermagem"
    else:
        tipo = "enfermagem"

    tipo_id = con.sql(f"SELECT id FROM tipoequipamento WHERE nome = '{tipo}'").fetchdf()['id'].iloc[0]
    tratamentos = con.sql(f"SELECT id, descricao, restricoes FROM tratamento WHERE id_tipoequipamento = {tipo_id}").fetchdf()

    if not tratamentos.empty:
        tratamento = tratamentos.sample(n=1).iloc[0]
        observacoes = f"{fake.text(max_nb_chars=20)}"

    data.append((
        idx + 1,
        str(row['id_paciente']),
        str(row['id_sala']),
        str(tratamento['id']),
        str(row['id_medico']),
        row['data'],
        observacoes
    ))

data = pd.DataFrame(data)

con.sql("""
            INSERT INTO prontuario SELECT * FROM data
        """)

# equipamentoativo (id, id_equipamento, data)
n_equipamentosativos = 15
numeros_unicos = random.sample(range(1, n_equipamentos + 1), n_equipamentosativos)

data = []
for i, num in enumerate(numeros_unicos):
    data.append(
        (
            i + 1,
            num,
            date.today()
        )
    )
data = pd.DataFrame(data)

con.sql("""
            INSERT INTO equipamentoativo SELECT * FROM data
        """)