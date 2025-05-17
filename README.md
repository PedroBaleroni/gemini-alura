# Quiz de Aprendizado

Um aplicativo de quiz simples construído em Python usando Tkinter, com a capacidade de integrar com a API Gemini para geração e validação de perguntas.

## Funcionalidades

* Seleção do ano escolar (5º ao 9º ano).
* Entrada de matéria ou tema para o quiz.
* Geração de perguntas (placeholder, com integração API Gemini planejada).
* Múltipla escolha com 5 opções de resposta.
* Botão de Dica para ajudar a encontrar a resposta.
* Feedback imediato (Acertou/Errou).
* Opção "Não Sei" para pular a pergunta.
* Opção "Sair" para encerrar o quiz e ver a pontuação final.
* Estrutura modular do código para fácil manutenção.
* (Planejado) Utilização da API Gemini para gerar perguntas relevantes para a série/tema e validar a qualidade das perguntas/respostas/dicas.

## Pré-requisitos

* Python 3.6 ou superior instalado.
* A biblioteca `tkinter` (geralmente incluída na instalação padrão do Python).
* A biblioteca `google-generativeai` (necessária para a integração com a API Gemini).

## Instalação

1.  **Clone ou faça download do repositório:**
    ```bash
    git clone <url_do_seu_repositório>
    # Ou baixe os arquivos diretamente
    ```
    Certifique-se de que os arquivos `main.py`, `quiz_app.py`, `gui_frames.py`, e `gemini_api.py` estão na mesma pasta (por exemplo, `quiz_project/`).

2.  **Instale a biblioteca `google-generativeai`:**
    Abra o terminal ou prompt de comando e execute:
    ```bash
    pip install google-generativeai
    ```

## Configuração da API Gemini

Para que o quiz utilize a inteligência artificial do Gemini para gerar e validar perguntas (conforme planejado na estrutura do código), você precisará de uma Chave de API.

1.  **Obtenha sua Chave de API:**
    * Vá para o [Google AI Studio](https://aistudio.google.com/).
    * Faça login com sua conta Google.
    * Crie uma nova chave de API (vá para "Get API key" no menu lateral).
    * Copie a chave gerada. **Guarde-a em segurança e não a compartilhe publicamente.**

2.  **Configure a Chave no Projeto:**
    * Abra o arquivo `gemini_api.py` no seu editor de código.
    * Encontre a seção "Gemini API Configuration (Placeholder)".
    * Substitua `"YOUR_GEMINI_API_KEY"` pela sua chave de API obtida no passo anterior.

    ```python
    # --- Gemini API Configuration (Placeholder) ---
    # Replace with your actual API key and configuration
    API_KEY = "SUA_CHAVE_DA_API_AQUI" # <--- COLOQUE SUA CHAVE AQUI
    # import google.generativeai as genai # Uncomment and install if you have the API setup

    # if API_KEY != "YOUR_GEMINI_API_KEY": # Check if the key was updated
    #     genai.configure(api_key=API_KEY)
    # else:
    #     print("Warning: Gemini API key not configured. Using placeholder data.")

    # ... restante do código ...
    ```

    * **Importante:** O código atual possui a integração da API **comentada** por padrão e usa dados estáticos. Para ativar a geração e validação via API, você precisará **descomentar** as linhas relacionadas à API Gemini no arquivo `gemini_api.py` e implementar a lógica de chamada da API dentro da função `generate_question`. A lógica de fallback para dados estáticos será usada se a API falhar ou não estiver configurada.

## Como Executar

1.  Abra o terminal ou prompt de comando.
2.  Navegue até a pasta onde você salvou os arquivos do projeto (por exemplo, `cd gemini_alura`).
3.  Execute o arquivo principal `main.py`:
    ```bash
    python main.py
    ```

A janela do aplicativo de quiz deverá ser exibida.

## Estrutura do Projeto

* `main.py`: O ponto de entrada da aplicação. Inicializa a janela Tkinter e a classe principal do quiz.
* `quiz_app.py`: Contém a classe principal `QuizApp` que gerencia o estado do quiz, a transição entre as telas e a lógica do jogo. Interage com `gui_frames.py` e `gemini_api.py`.
* `gui_frames.py`: Contém funções que criam e configuram os diferentes frames (telas) da interface gráfica (seleção, quiz, feedback, score).
* `gemini_api.py`: Responsável pela interação com a API Gemini (planejado) para gerar e validar perguntas, e pelo carregamento dos dados do quiz (atualmente usa dados estáticos como placeholder).

## Tópicos Interessantes e Próximos Passos

* **Implementar a Lógica da API Gemini:** A parte mais complexa e interessante é implementar a chamada real à API Gemini na função `gemini_api.py`. Isso envolverá engenharia de prompt cuidadosa para garantir que o modelo gere perguntas, respostas e dicas de alta qualidade e relevantes para a série/tema, além de validar se o conteúdo gerado atende aos critérios.
* **Melhorar a Validação:** A validação `curricular` e `answers_hints` (presente na estrutura placeholder) é crucial. Refine os prompts para a API Gemini para obter validações precisas.
* **Expandir os Dados Estáticos:** Enquanto a integração com a API não estiver completa ou como um fallback robusto, adicione mais perguntas aos dicionários `STATIC_QUIZ_DATA` em `gemini_api.py` para cobrir mais séries e temas.
* **Refinar a Interface Gráfica:** A interface Tkinter é funcional, mas pode ser aprimorada visualmente (cores, fontes, layouts).
* **Adicionar Mais Tipos de Perguntas:** Atualmente, é múltipla escolha. Você poderia expandir para outros formatos (resposta curta, verdadeiro/falso, etc.).
* **Gerenciamento de Erros da API:** Implementar um tratamento de erros mais robusto para falhas na comunicação com a API Gemini.
* **Armazenamento de Perguntas Geradas:** Considere salvar as perguntas geradas pela API (depois de validadas) em um arquivo (JSON, banco de dados) para evitar chamadas repetidas para o mesmo tema/série.

Este README fornece um guia completo para configurar e executar o projeto, além de destacar as áreas onde a integração com a API Gemini se encaixa e como o projeto pode ser expandido.