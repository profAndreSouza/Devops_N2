# 🚀 Plataforma de Ciência de Dados em Python (Devops N2)

Aplicação web desenvolvida em **Flask** para a disciplina de **Devops N2**, estruturada para a colaboração entre **1 Professor e 37 Alunos**.

A plataforma conta com um Dashboard Hub interativo, uma **Página Pública de Tarefas** e 37 módulos Python independentes em `features/`, onde cada aluno desenvolve uma funcionalidade completa do pipeline de Ciência de Dados.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3, Flask 3.x, Jinja2
- **Data Science**: Pandas, NumPy, Scikit-learn
- **Visualização**: Plotly.js, Seaborn, Matplotlib
- **Frontend**: HTML5, CSS3 Custom, Bootstrap 5, JavaScript (AJAX)

---

## 📁 Estrutura do Projeto

```
Devops_N2/
├── app.py                      # Servidor Flask e gerenciador de rotas/API
├── requirements.txt            # Dependências do projeto
├── README.md                   # Instruções e visão geral do projeto
├── TASKS.md                    # Documentação técnica e pública das 37 tarefas
├── utils/
│   └── data_loader.py          # Carregador de datasets de demonstração (Iris, Titanic, Wine, etc.)
├── static/
│   ├── css/style.css           # Estilização visual (Tema escuro/moderno)
│   └── js/main.js             # Scripts para gráficos interativos (Plotly)
├── templates/
│   ├── base.html               # Template base com Navbar e Footer
│   ├── index.html              # Dashboard Hub dos 37 alunos
│   ├── tasks_public.html       # Página Pública das 37 Tarefas dos Alunos
│   └── task_detail.html        # Executor visual da tarefa selecionada
└── features/                   # Módulos Python individuais dos 37 Alunos
    ├── __init__.py
    ├── task_01_upload_schema.py
    ├── task_02_missing_values.py
    ├── ...
    └── task_37_report_generator.py
```

---

## ⚡ Como Executar a Aplicação

### Opção 1: Com Docker Compose (Recomendado)

1. Suba o container com um único comando:
   ```bash
   docker-compose up --build
   ```
2. Acesse no seu navegador: `http://localhost:5000`

---

### Opção 2: Diretamente via Python

1. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

2. Inicie o servidor Flask:
   ```bash
   python app.py
   ```

3. Acesse no seu navegador:
   - **Dashboard Hub**: `http://localhost:5000`
   - **Tarefas Públicas**: `http://localhost:5000/tasks`

---

## 🎓 Instruções para os 37 Alunos

1. Localize o seu arquivo correspondente dentro da pasta `features/` (exemplo: `task_05_encoding.py`).
2. Edite apenas a função `run_feature(df, params=None)` no seu arquivo.
3. Retorne um dicionário contendo os títulos, métricas, tabelas (`df.to_html()`) e gráficos (`fig.to_json()`).
4. Para testar sua alteração, abra a página da sua tarefa na aplicação e selecione um dos conjuntos de dados de teste.