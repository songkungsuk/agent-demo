from google.adk.agents import Agent
from .prompt import CONTENT_ANALYZER_AGENT_INSTRUCTION, CONTENT_ANALYZER_AGENT_DESCRIPTION

# content_analyzer 정의
content_analyzer = Agent(
   name="content_analyzer", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=CONTENT_ANALYZER_AGENT_INSTRUCTION, # prompt.py에서 가져온 설명
   instruction=CONTENT_ANALYZER_AGENT_DESCRIPTION, # prompt.py에서 가져온 지시문
)