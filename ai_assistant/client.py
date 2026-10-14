import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from PyQt6.QtCore import QObject, pyqtSignal

load_dotenv()
API_KEY = os.environ["API_KEY"]
FOLDER_ID = os.environ["FOLDER_ID"]

client = OpenAI(
    base_url = "https://ai.api.cloud.yandex.net/v1",
    api_key = API_KEY,
    project = FOLDER_ID
)
    
model = f"gpt://{FOLDER_ID}/yandexgpt/rc"

class RelaxSession(QObject):
    relax_trigger = pyqtSignal()

relax_bridge = RelaxSession()

def call_relax_session():
    relax_bridge.relax_trigger.emit()
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
                
                if function_name in self.function_map:
                    function_result = self.function_map[function_name](**function_args)
                    
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
1. Давать лаконичные рекомендации по улучшению осанки и защите зрения (не более 3 предложений).
2. Если пользователь жалуется на глаза или усталость, ты должен сначала вежливо ПРЕДЛОЖИТЬ ему провести разминку текстом (например: «Давай проведем разминку для глаз?»). В этот момент функцию call_relax_session вызывать НЕ НУЖНО.
3. ЕСЛИ пользователь явно соглашается на твое предложение («Давай», «Запускай», «Хочу», «Да»), вот тогда ты ОБЯЗАН вызвать функцию call_relax_session через инструменты tools. В самом текстовом ответе при этом не должно быть никаких JSON-структур или технических скобок.

Пиши кратко и по делу на русском языке.
"""
health_care_assistant = Assistant(instructions = instructions, tools=tools, function_map=my_functions)




