# Documentação Detalhada: Programa de Processamento e Consolidação de Arquivos Excel

## **Visão Geral**
Este programa é um script em Python projetado para automatizar o processo de leitura, transformação e consolidação de múltiplos arquivos Excel contidos em um diretório específico. Ele combina a simplicidade da biblioteca **Pandas** com ferramentas do sistema operacional para criar uma solução robusta e eficiente, adequada para fluxos de trabalho que exigem manipulação de dados estruturados.

O script:
1. Localiza automaticamente os arquivos Excel dentro de um diretório definido.
2. Extrai e processa os dados de cada arquivo, adicionando metadados personalizados.
3. Consolida os dados processados em um único arquivo Excel.
4. Salva o arquivo final em um local predefinido.

---

## **Requisitos e Configurações**

### Dependências
O script exige as seguintes ferramentas e bibliotecas:
- **Python 3.7 ou superior**
- Bibliotecas Python:
  - `pandas`: Para manipulação e análise de dados.
  - `os`: Para operações com o sistema de arquivos.
  - `glob`: Para buscar arquivos com padrões específicos.
  - `xlsxwriter`: Para salvar arquivos Excel com eficiência.

### Estrutura de Diretórios
O programa pressupõe que os arquivos de entrada e saída sejam organizados em uma estrutura de diretórios como esta:
```
src/
├── data/
│   ├── raw/      # Diretório de entrada contendo os arquivos Excel originais.
│   ├── ready/    # Diretório de saída para armazenar o arquivo consolidado.
```

---

## **Fluxo do Programa**

### 1. **Configuração do Caminho de Entrada**
O programa inicia definindo o caminho da pasta onde estão localizados os arquivos Excel a serem processados:
```python
folder_path = 'src\\data\\raw'
```
Em seguida, utiliza o módulo **glob** para localizar todos os arquivos com extensão `.xlsx`:
```python
excel_files = glob.glob(os.path.join(folder_path, '*.xlsx'))
```
Se nenhum arquivo for encontrado, o programa exibe:
```plaintext
Nenhum arquivo encontrado
```

---

### 2. **Processamento de Arquivos**
Se arquivos Excel forem encontrados, o programa inicia um loop para processar cada um deles. Esse processo consiste nas seguintes etapas:

#### a. **Leitura do Arquivo**
Cada arquivo é carregado em um DataFrame temporário:
```python
df_temp = pd.read_excel(file)
```

#### b. **Extração do Nome do Arquivo**
O nome do arquivo é extraído para identificar possíveis metadados:
```python
file_name = os.path.basename(file)
```

#### c. **Adição de Colunas Personalizadas**
Duas colunas são adicionadas ao DataFrame:
- **Coluna `country`:**
  Baseada em palavras-chave no nome do arquivo:
  - `"brasil"` no nome do arquivo adiciona o valor `"br"`.
  - `"france"` no nome do arquivo adiciona o valor `"fr"`.
  - `"italian"` no nome do arquivo adiciona o valor `"it"`.
  ```python
  if 'brasil' in file_name.lower():
      df_temp['country'] = 'br'
  elif 'france' in file_name.lower():
      df_temp['country'] = 'fr'
  elif 'italian' in file_name.lower():
      df_temp['country'] = 'it'
  ```

- **Coluna `campaign`:**
  Extraída do campo `utm_link` por meio de uma expressão regular que identifica o parâmetro `utm_campaign`:
  ```python
  df_temp['campaign'] = df_temp['utm_link'].str.extract(r'utm_campaign=(.*)')
  ```

#### d. **Armazenamento Temporário**
O DataFrame processado é adicionado a uma lista para posterior consolidação:
```python
df.append(df_temp)
```

#### e. **Tratamento de Erros**
Erros que ocorram durante o processamento de um arquivo são capturados e exibidos com detalhes:
```python
except Exception as e:
    print(f"Erro ao ler o arquivo {file} : {e}")
```

---

### 3. **Consolidação dos Dados**
Após o processamento de todos os arquivos, o programa verifica se há dados a consolidar:
- **Concatenação:**
  Os DataFrames armazenados na lista são combinados em um único DataFrame:
  ```python
  result = pd.concat(df, ignore_index=True)
  ```

- **Salvamento do Arquivo Consolidado:**
  O DataFrame consolidado é salvo em um novo arquivo Excel no diretório `src/data/ready`. O motor **xlsxwriter** é utilizado para maior eficiência:
  ```python
  out_file = os.path.join('src', 'data', 'ready', 'clean.xlsx')
  writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
  result.to_excel(writer, index=False)
  writer.close()
  ```

- **Ausência de Dados:**
  Caso nenhum dado tenha sido processado, o programa informa:
  ```plaintext
  Nenhum arquivo encontrado
  ```

---

## **Mensagens de Saída**
O script fornece mensagens úteis durante a execução:
- **Nenhum Arquivo Encontrado:** Informa que não foram localizados arquivos `.xlsx` no diretório de entrada.
- **Erro ao Ler o Arquivo:** Fornece detalhes sobre problemas encontrados ao processar arquivos específicos.
- **Impressão dos DataFrames Processados:** Cada DataFrame temporário é exibido no console para validação manual durante a execução.

---

## **Considerações Técnicas**
1. **Estrutura Modular:**
   O programa é dividido em etapas lógicas que podem ser adaptadas ou reutilizadas em outros projetos.

2. **Tratamento de Erros:**
   A implementação de `try-except` assegura que problemas em arquivos específicos não interrompam a execução completa do programa.

3. **Flexibilidade:**
   - Adição de colunas com base no nome do arquivo permite processar dados de diferentes países ou campanhas.
   - O uso de expressões regulares facilita a extração de parâmetros específicos em campos de texto.

4. **Manutenção:**
   - O código pode ser facilmente atualizado para incluir novos critérios de metadados ou suportar diferentes tipos de arquivos.

---

## **Possíveis Melhorias**
- **Suporte a Outros Formatos:** Adicionar suporte para arquivos CSV ou Excel em outros formatos, como `.xlsm`.
- **Validação Avançada:** Implementar verificações para assegurar a consistência dos dados (e.g., colunas obrigatórias).
- **Interface Gráfica:** Criar uma interface gráfica ou CLI interativa para seleção de diretórios e configurações.
- **Log de Execução:** Implementar um sistema de log detalhado para armazenar erros e eventos.

Este script é ideal para tarefas de ETL (Extração, Transformação e Carregamento) e pode ser adaptado para diferentes cenários de processamento de dados estruturados.
