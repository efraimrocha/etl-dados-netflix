# Documentação do Programa: Processamento e Consolidação de Arquivos Excel com Pandas

## **Descrição Geral**
Este programa é um script em Python projetado para automatizar o processamento e a consolidação de arquivos Excel armazenados em uma pasta específica. Ele utiliza as bibliotecas **Pandas**, **os**, e **glob** para:
1. Identificar e carregar arquivos Excel em um diretório.
2. Extrair informações relevantes de cada arquivo.
3. Adicionar metadados baseados em regras específicas.
4. Consolidar os dados em um único arquivo Excel de saída, pronto para análise ou uso posterior.

---

## **Requisitos**
### Dependências
- **Python 3.7+**
- Bibliotecas:
  - `pandas`
  - `os`
  - `glob`
  - `xlsxwriter`

### Estrutura de Diretórios
- O script pressupõe a seguinte estrutura de diretórios:
  ```
  src/
  ├── data/
       ├── raw/      # Diretório contendo os arquivos Excel de entrada.
       ├── ready/    # Diretório onde o arquivo consolidado será salvo.
  ```

---

## **Funcionamento**

### 1. **Identificação dos Arquivos**
O programa inicia configurando o diretório `src/data/raw` como o local para buscar arquivos Excel. Ele usa o módulo **glob** para identificar todos os arquivos com extensão `.xlsx`.

- **Caminho configurado:**
  ```python
  folder_path = 'src\\data\\raw'
  excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))
  ```

- **Tratamento de erros:**
  Caso nenhum arquivo seja encontrado, uma mensagem será exibida:
  ```plaintext
  Nenhum arquivo encontrado
  ```

---

### 2. **Processamento de Arquivos**
Para cada arquivo Excel encontrado:
1. **Carregamento:**
   - Os dados do arquivo são lidos para um DataFrame usando `pd.read_excel`.

2. **Extração do Nome do Arquivo:**
   - O nome do arquivo é extraído usando `os.path.basename`.

3. **Adição de Metadados:**
   - **Coluna `country`:** Baseada em palavras-chave no nome do arquivo:
     - `"brasil"` -> `"br"`
     - `"france"` -> `"fr"`
     - `"italian"` -> `"it"`
   - **Coluna `campaign`:** Extraída do campo `utm_link` com uma expressão regular para identificar o parâmetro `utm_campaign`.

4. **Armazenamento Temporário:**
   - O DataFrame processado é adicionado a uma lista de DataFrames para posterior consolidação.

5. **Tratamento de Erros:**
   - Caso ocorra qualquer problema ao processar o arquivo, o erro é capturado e exibido:
     ```plaintext
     Erro ao ler o arquivo {file} : {mensagem de erro}
     ```

---

### 3. **Consolidação dos Dados**
Após o processamento de todos os arquivos:
- **Concatenação:**
  - Os DataFrames armazenados são concatenados em um único DataFrame:
    ```python
    result = pd.concat(df, ignore_index=True)
    ```

- **Criação do Arquivo Consolidado:**
  - O arquivo consolidado é salvo no diretório `src/data/ready` com o nome `clean.xlsx`.
  - Para isso, é utilizado o motor `xlsxwriter`:
    ```python
    writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
    result.to_excel(writer, index=False)
    writer.close()
    ```

- **Tratamento de Ausência de Dados:**
  - Caso não haja dados processados, o programa exibe:
    ```plaintext
    Nenhum arquivo encontrado
    ```

---

## **Detalhes Técnicos**
1. **Criação de Colunas Personalizadas:**
   - A coluna `country` é criada baseada em palavras-chave do nome do arquivo.
   - A coluna `campaign` é gerada a partir de links UTM presentes no campo `utm_link`.

2. **Tratamento de Erros:**
   - O programa utiliza `try-except` para capturar exceções durante a leitura de arquivos.

3. **Configuração do Caminho de Saída:**
   - O caminho de saída do arquivo consolidado é gerado dinamicamente usando `os.path.join`.

4. **Garantia de Fechamento do Writer:**
   - O método `writer.close()` é utilizado para assegurar que o arquivo de saída seja salvo corretamente.

---

## **Mensagens de Saída**
- **Nenhum Arquivo Encontrado:** Indica que a pasta de entrada não possui arquivos `.xlsx`.
- **Erro ao Ler o Arquivo:** Detalha problemas ocorridos ao processar arquivos específicos.
- **Impressão dos DataFrames:** Cada DataFrame processado é exibido no console para fins de verificação.

---

## **Considerações**
Este programa é ideal para fluxos de trabalho que envolvem:
- Integração e análise de dados de diferentes fontes.
- Automação de tarefas repetitivas de processamento de arquivos Excel.
- Preparação de dados para análise em larga escala.
