import random
import google.generativeai as genai
import json

# --- Gemini API Configuration (Placeholder) ---
# Replace with your actual API key and configuration

API_KEY = "AIzaSyBA2N7NVl8wOanaLxr7SUnbDugioircsY8"

if API_KEY != "YOUR_GEMINI_API_KEY":
    genai.configure(api_key=API_KEY)
else:
    print("Warning: Gemini API key not configured. Using placeholder data.")


def generate_question(grade, topic):
    """
    Calls Gemini API to generate a question, answers, and hint.
    Also requests validation.
    Returns: dictionary with question_text, options_dict, correct_answer_key, hint, validation_status
    """
    if API_KEY == "YOUR_GEMINI_API_KEY":
         print("Gemini API key not set. Cannot generate questions via API.")
         return None # Cannot generate without key

    try:
        # Example prompt - needs refinement for actual use
        model = genai.GenerativeModel('gemini-1.5-flash-latest') # Escolha um modelo apropriado

        prompt = f"""
        Generate, in brazillian portuguese, a simple quiz question suitable for a {grade} of elemental school, student about {topic}.
        The question should be no more than 3 lines long.
        Provide 5 single-line multiple-choice options (A, B, C, D, E).
        Indicate the correct answer key (A, B, C, D, or E).
        Provide a simple hint (one line) to help find the answer.
        Also, validate if this question is likely within the typical curriculum for a {grade} student.
        Finally, validate if the provided answer options include the correct answer and if the hint is helpful.

        Format the output as a JSON object with the following keys:
        {{
            "question": "...",
            "options": {{"A": "...", "B": "...", "C": "...", "D": "...", "E": "..."}},
            "correct_answer": "A", # Or B, C, D, E
            "hint": "...",
            "validation": {{"curricular": true/false, "answers_hints": true/false}}
        }}
        **IMPORTANT:** Enclose the JSON output within a Markdown code block like this: ```json ... ```
        """
        
        print("Sending prompt to Gemini API...")
        response = model.generate_content(prompt)

        print("Received response text from Gemini API:")
        print(response.text) # Imprime a resposta bruta para debug

        # --- EXTRAÇÃO DO JSON ---
        response_text = response.text.strip() # Remove espaços em branco do início/fim
        if response_text.startswith("```json") and response_text.endswith("```"):
            # Encontra o início e o fim do bloco JSON e extrai o conteúdo
            json_string = response_text[len("```json"):].rstrip("```").strip()
        else:
            # Se não estiver no formato esperado, assume que a resposta inteira é o JSON (menos comum)
            json_string = response_text
            print("Warning: API response was not enclosed in ```json ```. Attempting to parse directly.")
        # --- FIM DA EXTRAÇÃO ---


        # Tenta parsear o JSON extraído APENAS SE json_string NÃO estiver vazio
        if json_string:
            data = json.loads(json_string) # Tenta parsear o JSON extraído

            print("Parsed JSON data:")
            print(data)

            return data # Retorna os dados se tudo der certo
        else:
            print("Extracted JSON string was empty.") # Mensagem se a string extraída estiver vazia
            return None

    except json.JSONDecodeError as e:
         print(f"Error decoding JSON from extracted string: {e}")
         print("String being parsed:", json_string) # Imprime a string que falhou
         return None
    except Exception as e:
        print(f"An unexpected error occurred during Gemini API call or processing: {e}")
        return None


# --- Placeholder Data (for testing without API) ---
# This data simulates the output structure expected from generate_question
STATIC_QUIZ_DATA = {
    "5º Ano": [
        {
            "question": "Qual é o resultado de 15 + 23?",
            "options": {"A": "38", "B": "40", "C": "35", "D": "42", "E": "37"},
            "correct_answer": "A",
            "hint": "É uma adição simples.",
            "validation": {"curricular": True, "answers_hints": True}
        },
        {
            "question": "Quantos lados tem um quadrado?",
            "options": {"A": "3", "B": "4", "C": "5", "D": "6", "E": "2"},
            "correct_answer": "B",
            "hint": "Pense em uma caixa.",
            "validation": {"curricular": True, "answers_hints": True}
        },
         {
            "question": "O que é um substantivo próprio?",
            "options": {"A": "Nome de coisas", "B": "Nome de lugares ou pessoas específicos", "C": "Nome de ações", "D": "Palavras que indicam qualidade", "E": "Palavras que ligam frases"},
            "correct_answer": "B",
            "hint": "Pense no nome de sua cidade ou de um amigo.",
            "validation": {"curricular": True, "answers_hints": True}
        }
    ],
    "9º Ano": [
        {
            "question": "Qual a fórmula da área de um círculo?",
            "options": {"A": "πr²", "B": "2πr", "C": "lado²", "D": "base x altura / 2", "E": "πd"},
            "correct_answer": "A",
            "hint": "Envolve Pi e o raio.",
            "validation": {"curricular": True, "answers_hints": True}
        },
         {
            "question": "Quem escreveu 'O Alienista'?",
            "options": {"A": "Machado de Assis", "B": "Jose de Alencar", "C": "Carlos Drummond de Andrade", "D": "Clarice Lispector", "E": "Monteiro Lobato"},
            "correct_answer": "A",
            "hint": "Um famoso escritor brasileiro do século XIX.",
            "validation": {"curricular": True, "answers_hints": True}
        },
        {
             "question": "Calcule o valor de x na equação:\n2x + 5 = 15",
             "options": {"A": "5", "B": "10", "C": "2", "D": "7", "E": "8"},
             "correct_answer": "A",
             "hint": "Primeiro, subtraia 5 dos dois lados da equação.",
             "validation": {"curricular": True, "answers_hints": True}
        }
    ]
    # Add more static data for other grades if needed
}


def load_quiz_data(grade, topic, num_questions=5):
    """
    Loads or generates quiz data for the given grade and topic.
    In a real app, this would primarily use the Gemini API.
    For now, it uses static data and shuffles it.
    """
    generated_questions = []

    # --- API Data Generation (Commented Out) ---
    if API_KEY != "YOUR_GEMINI_API_KEY":
        print(f"Attempting to generate {num_questions} questions for {grade} - {topic} using Gemini API...")
        for _ in range(num_questions * 2): # Try to generate more than needed as some might be invalid
            question_data = generate_question(grade, topic)
            if question_data and question_data.get("validation", {}).get("curricular", False) and question_data.get("validation", {}).get("answers_hints", False):
                generated_questions.append(question_data)
                if len(generated_questions) >= num_questions:
                    break
        if generated_questions:
             random.shuffle(generated_questions)
             return generated_questions[:num_questions]
        else:
             print("Failed to generate valid questions from API. Falling back to static data if available.")
    # --- End API Data Generation ---

    # --- Fallback to Static Data ---
    print(f"Using static quiz data for {grade}...")
    static_questions = STATIC_QUIZ_DATA.get(grade, [])
    if static_questions:
        # Filter static data by topic if needed (more complex without API validation)
        # For simplicity here, we just shuffle the relevant grade's data
        shuffled_questions = list(static_questions) # Create a copy before shuffling
        random.shuffle(shuffled_questions)
        return shuffled_questions[:num_questions] # Return a limited number of questions
    else:
        print(f"No static data available for {grade}.")
        return []