from google.adk.agents import Agent
from api_agents.nexon_api_agent.agent import nexon_api_agent
from api_agents.riot_api_agent.agent import riot_api_agent
from .prompt import ROOT_AGENT_DESCRIPTION, ROOT_AGENT_INSTRUCTION

# root_agent 정의
root_agent = Agent(
   name="root_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=ROOT_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=ROOT_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   sub_agents=[
       nexon_api_agent,
       riot_api_agent,
   ]
)
