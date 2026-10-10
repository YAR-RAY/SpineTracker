import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from openai import OpenAI
from dotenv import load_dotenv
from ui_notification.relax_window import open_relax_window
import json

load_dotenv()
API_KEY = os.environ["API_KEY"]
FOLDER_ID = os.environ["FOLDER_ID"]

client = OpenAI(
    base_url = "https://ai.api.cloud.yandex.net/v1",
    api_key = API_KEY,
    project = FOLDER_ID
)
    
model = f"gpt://{FOLDER_ID}/yandexgpt/rc"

def call_relax_session():
    print('функция вызвана')
    open_relax_window()
    return {"status": "success", "message": "Окно разминки успешно открыто на экране пользователя."}
my_functions = {
    "call_relax_session": call_relax_session
}

class Assistant:
    def __init__(self, instructions, tools=None, model=model, function_map=None):
        self.model = model
        self.instructions = instructions
        self.tools = tools or []
        self.previous_response_id_map = {}
        self.function_map = function_map
    def __call__(self, input_text, session_id='default'):
        previous_response_id = self.previous_response_id_map.get(session_id, None)
        response = client.responses.create(
            model = self.model,
            store = True,
            instructions = self.instructions,
            previous_response_id = previous_response_id,
            input = input_text,
            tools = self.tools
        )
        self.previous_response_id_map[session_id] = response.id
        return self._process_response(response, session_id)
    def _process_response(self, response, session_id):
        for output_item in response.output:
            if output_item.type == "function_call":
                function_name = output_item.name
                arguments_str = output_item.arguments
                
                function_args = json.loads(arguments_str)
                
                print(f"[DEBUG] Вызов функции: {function_name}({function_args})")
                
                if function_name in self.function_map:
                    function_result = self.function_map[function_name](**function_args)
                    
                    print(f"[DEBUG] Результат функции: {function_result}")
                    
                    result_message = f"Результат выполнения функции {function_name}: {json.dumps(function_result, ensure_ascii=False)}"
                    
                    follow_up = client.responses.create(
                        model=self.model,
                        store=True,
                        previous_response_id=response.id,
                        input=result_message
                    )
                    
                    self.previous_response_id_map[session_id] = follow_up.id
                    
                    return self._process_response(follow_up, session_id)
        
        final_text = response.output_text if hasattr(response, 'output_text') else ""
        return final_text
    
tools = [
    {
        "type": "function",
        "name": "call_relax_session",
        "description": "Открывает окно с разминкой для глаз",
        "parameters": {
            "type": "object",
            "properties": {}, 
            "required": []
        }
    }
]

instructions = """
Ты — профессиональный врач-эргономист. К тебе обращается пользователь за помощью.
Твоя задача:
1. Давать лаконичные и практичные рекомендации по улучшению осанки и защите зрения.
2. Отвечать на вопросы пользователя дружелюбно и коротко (не более 3 предложений).
3. ЕСЛИ пользователь просит сделать тренировку, разминку или упражнение для глаз, ты ОБЯЗАН вызвать функцию call_relax_session ").

Пиши кратко и по делу.
"""


health_care_assistant = Assistant(instructions = instructions, tools=tools, function_map=my_functions)
#print(health_care_assistant("давай разминку для глаз"))




'''
def __init__(self, model=model, instructions=None, tools=None, function_map=None):
        self.model = model
        self.instructions = instructions
        self.tools = tools or []
        self.function_map = function_map

    def __call__(self, input_text, session_id='default'):
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": f"{self.instructions}\n\nПользователь спрашивает: {input_text}"}
                ],
                temperature=0.6
            )
            
            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content
                
            return "Сервер вернул пустой ответ."
            
        except Exception as e:
            return f"Ошибка подключения к YandexGPT: {e}"
и ОДНОВРЕМЕННО написать пользователю в чат вежливое подтверждение (например: "Конечно, я запускаю окно разминки. Отвлекитесь от экрана на 20 секунд!
, но всегда возвращай текстовый ответ, чтобы пользователь видел твои реплики в чате
            
            
            '''