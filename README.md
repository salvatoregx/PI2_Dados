# Projeto Integrador 2: Rastreamento de equipamentos hospitalares

Este projeto foi desenvolvido para a disciplina **Projeto Integrador 2** dos cursos tecnólogos do Senac EAD. Simula um sistema de gestão hospitalar focado no rastreamento e manutenção dos equipamentos, com geração de dados fictícios, utilizados para fluxos ETL e análises em BI. É baseado em Python e DuckDB, e utiliza Poetry para gerenciamento de dependências.

## 🛠️ Tecnologias

- **Python 3.10+**: Linguagem principal para scripts e lógica.
- **Poetry**: Gerenciador de dependências ([instalação](https://python-poetry.org/docs/)).
- **DuckDB**: Banco de dados embutido para análises rápidas ([documentação](https://duckdb.org/docs/stable/)).
- **Pandas**: Manipulação de dados tabulares.
- **Faker**: Geração de dados fictícios.
- **Jupyter Lab**: Simulação de fluxos ETL e análises descritivas.
- **Plotly**: Geração de visualizações interativas.

## 📥 Instalação

**Clone o repositório:**
```bash
git clone https://github.com/salvatoregx/PI2_Dados.git
cd PI2_Dados
```

**Instale as dependências:**
```bash
poetry install
```

## 📁 Estrutura do Projeto

PI2_Dados \
├── src \
│   ├── listas \
│   │   ├── especialidades.txt \
│   │   ├── insumos.txt \
│   │   ├── siglas_estados.txt \
│   │   ├── tipoequipamento.txt \
│   │   └── tratamentos.csv \
│   └── pi2_dados \
│   │   ├── __init__.py \
│   │   ├── __main__.py \
│   │   ├── pi2_cria_dados.py \
│   │   ├── pi2_cria_tabelas.py \
│   │   └── pi2_remove_tabelas.py \
├── Exemplos.ipynb \
├── ETL_e_Análises.ipynb \
├── LICENSE \
├── pi2_solucao_hospitalar.db \
├── poetry.lock \
├── pyproject.toml \
└── README.md


## 🚀 Como Executar

**Para executar o menu de criação de tabelas e dados**
```bash
poetry run python -m pi2_dados
```

**Para executar análises ETL e visualizações:**
```bash
poetry run jupyter lab
```

## 💡 Exemplos de Uso

**ETL e Análises (Jupyer Lab):**
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salvatoregx/PI2_Dados/HEAD?urlpath=%2Fdoc%2Ftree%2FETL_e_An%C3%A1lises.ipynb) \
O notebook ETL_e_Análises.ipynb simula fluxos ETL e contém a execução das seguintes análises: \
    1. Gráfico de barras de internações por setor \
    2. Agenda de manutenções preventivas \
    3. Utilização de tratamentos por tipo de equipamento \
    4. Radar de ocupação de leitos
    

**Consulta Básica (Python):**
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/salvatoregx/PI2_Dados/HEAD?urlpath=%2Fdoc%2Ftree%2FExemplos.ipynb) \
```python
import duckdb
con = duckdb.connect("pi2_solucao_hospitalar.db")
```

### Listar 5 pacientes
```python
pacientes = con.sql("SELECT * FROM paciente LIMIT 5").fetchdf()
print(pacientes)
```

### Total de internações por setor
```python
internacoes_setor = con.sql("""
    SELECT s.setor, COUNT(i.id) AS total
    FROM internacao i
    JOIN sala s ON i.id_sala = s.id
    GROUP BY s.setor
""").fetchdf()
```

### Análise de Equipamentos Ativos
```python
equipamentos_ativos = con.sql("""
    SELECT e.modelo, COUNT(a.id) AS total_ativos
    FROM equipamentoativo a
    JOIN equipamento e ON a.id_equipamento = e.id
    GROUP BY e.modelo
""").fetchdf()
```
