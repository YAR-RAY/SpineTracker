from openai import OpenAI
from config import api_key, folder_id


client = OpenAI(
    base_url = "https://ai.api.cloud.yandex.net/v1",
    api_key = api_key,
    project = folder_id)

model = f'gpt://{folder_id}/yandexgpt/rc'

class Assistant:
    def __init__(self, model=model,instructions=None, tools=None, function_map=None):
        self.model = model,
        self.instructions = instructions,
        self.tools = tools or [],
        self.function_map = function_map
    def __call__(self, input_text, session_id = 'default'):
        response = client.responses.create(
            model = self.model,
            store = True,
            instructions = self.instructions,
            tools = self.tools, 
            input = input_text
        )
        return response.output_text if hasattr(response, 'output_text') else "" 
instructions = """
Ты - профессиональный врач, который работает с проблемами из-за компьютера. К тебе будет обращаться пользователь за рекомендациями.
Твоя задача - помогать пользователям:
1. Давать краткие рекомендации по поводу их проблемы
2. Отвечать на возникшие вопросы
3. Давать краткий план действий для быстрого решения их проблемы

Говори, учитвая что это происходит во время рабочего дня, сессии. Ты должен минимально занимать время: писать кратко, не уходить в объяснения и рассуждения. Кратко и по делу
"""

health_care_assistant = Assistant(instructions)
print(health_care_assistant("Что делать с уставшими глазами"))