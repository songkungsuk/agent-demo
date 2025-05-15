from google.adk.agents import Agent
from .prompt import RIOT_API_AGENT_DESCRIPTION, RIOT_API_AGENT_INSTRUCTION
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Any, Optional

# 프로젝트 루트 디렉토리 찾기
project_root = Path(__file__).parent.parent

# .env 파일 경로 지정
env_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=env_path)

# 환경 변수 사용
RIOT_API_KEY = os.getenv("RIOT_API_KEY")

# league of lengend 정보 검색 기능
def use_riot_api(name : str) -> dict[str, Any]:
   """
   리그오브레전드의 소환사 검색 기능입니다
   사용자가 입력한 이름의 롤, 리그오브레전드의 정보를 물어볼때 사용하면 됩니다.
   """
   
   if not len(name.split("#")) == 2:
      return {"message" : "소환사의 이름을 태그와 함께 써주세요"}
   
   header = {
      "Origin" : "https://developer.riotgames.com",
      "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
      "Accept-Charset" : "application/x-www-form-urlencoded; charset=UTF-8",
      "Accept-Language" : "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
   }
   
   url_puuid = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + name.split("#")[0] + "/" + name.split("#")[1]
   response = requests.get(url_puuid, params={"api_key" : RIOT_API_KEY}, headers=header)
   
   puuid = response.json().get('puuid')
   
   if not puuid:
      return {"message" : "Data not found - No results found for player with riot id " + name}
   
   league_url = f"https://kr.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
   match_list_url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
   
   league_response = requests.get(league_url, params={"api_key" : RIOT_API_KEY}, headers=header)
   match_list_response = requests.get(match_list_url, params={"api_key" : RIOT_API_KEY}, headers=header)
   
   data = {
      "league_info" : league_response.json()
   }
   
   if match_list_response.status_code == 200:
      for match in match_list_response.json() :
         match_url = "https://asia.api.riotgames.com/lol/match/v5/matches/" + match
         match_response = requests.get(match_url, params={"api_key" : RIOT_API_KEY}, headers=header)
         data['match_number : ' + match] = match_response.json()
         
   return data         
   
   

# riot_api_agent 정의
riot_api_agent = Agent(
   name="riot_api_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=RIOT_API_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=RIOT_API_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   tools=[use_riot_api]
)