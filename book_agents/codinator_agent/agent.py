from google.adk.agents import Agent
from .prompt import CODINATOR_AGENT_DESCRIPTION, CODINATOR_AGENT_INSTRUCTION

# codinator_agent 정의
codinator_agent = Agent(
   name="codinator_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=CODINATOR_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=CODINATOR_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
)