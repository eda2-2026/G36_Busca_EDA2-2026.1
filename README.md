# SwiftPay

**Conteúdo da Disciplina**: Algoritmos de Busca em Memória (Busca Binária e Índice Invertido)<br>

## Alunos
|Matrícula | Aluno |
| -- | -- |
| 231026616 | Davi Emanuel Ribeiro de Oliveira |
| 202045769 | Gabriel Saraiva Canabrava |

## Sobre 
O projeto "SwiftPay" é um sistema web interativo voltado para auditoria e análise de transações financeiras. O objetivo principal é demonstrar a aplicação de algoritmos de busca otimizados da disciplina de Estrutura de Dados e Algoritmos 2 (EDA 2), utilizando **Índice Invertido** para campos categóricos e **Busca Binária** para dados ordenados (como datas e valores). Isso permite a filtragem de grandes volumes de transações de maneira quase instantânea, sem a necessidade de um banco de dados tradicional.

### Busca por Categorias e Lojas (Índice Invertido)
O sistema processa os dados no momento de inicialização e cria um índice invertido em memória para as categorias e nomes de lojas (merchants). Isso garante que consultas nesses atributos possuam tempo de busca logarítmico/constante, sendo executadas com complexidade de tempo **O(1)**.

### Filtros de Range (Busca Binária)
Para lidar com requisições compostas por intervalos — como buscas por um período de dias específicos ("Entre 01/01 e 31/01") ou por faixas de valores ("Entre R$ 50,00 e R$ 200,00") — o sistema emprega a busca binária sobre listas pré-ordenadas. Dessa forma, é possível localizar o início e o fim do intervalo rapidamente, com complexidade **O(log N)**.

## Screenshots
![Dashboard 1](SwiftPay/fotos/Captura%20de%20tela%202026-04-05%20191252.png)
![Dashboard 2](SwiftPay/fotos/Captura%20de%20tela%202026-04-05%20191312.png)
![Dashboard 3](SwiftPay/fotos/Captura%20de%20tela%202026-04-05%20191442.png)

## Instalação 
**Linguagem**: Python<br>
### Pré-requisitos:
* Python 3 instalado (Faça o download em python.org, se necessário).
* Bibliotecas listadas no arquivo requirements.txt (As dependências principais são Flask e Flask-CORS para rodar a nossa API web com Python).

### Passos para Instalação:
1. Clone este repositório para a sua máquina.
2. Navegue até a pasta do projeto:
```bash
    cd SwiftPay
```
3. Crie um ambiente virtual (opcional, mas recomendado):
```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
```
4. Instale as dependências:
```bash
    pip install -r backend/requirements.txt
```

## Uso 
1. Estando dentro do diretório `SwiftPay`, inicie a aplicação:
```bash
    python3 backend/app.py
```
2. Abra o seu navegador e acesse:
   **http://localhost:5000**
3. **Como testar os filtros de busca no painel:**
   * **Category / Categoria:** Pesquise por transações em um setor específico (ex: "Alimentação").
   * **Merchant / Loja:** Pesquise pelas transações de um comércio específico (ex: "Amazon").
   * **Min/Max Amount:** Filtre pelo valor transacionado. (ex: Mínimo = `10`, Máximo = `50`).
   * **Intervalo de Datas:** Especifique um período onde a compra ocorreu.
   * O sistema calculará o número de resultados e as estatísticas totais de forma automática enquanto garante o menor tempo de execução possível da busca.

## Video 

https://drive.google.com/file/d/1ZSF5Mez4a3K14Crxh4azekGw1yVM7u0C/view?usp=drive_link