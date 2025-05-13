from google.adk.agents import Agent
from book_agents.web_agent.agent import web_agent
from book_agents.analyze_agent.agent import analyze_agent
from .prompt import ANALYZE_AGENT_DESCRIPTION, ANALYZE_AGENT_INSTRUCTION

# root_agent 정의
root_agent = Agent(
   name="root_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=ANALYZE_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=ANALYZE_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   sub_agents=[
       web_agent,
       analyze_agent
   ]
)