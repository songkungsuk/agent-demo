from google.adk.agents import Agent
from .prompt import NEXON_API_AGENT_DESCRIPTION, NEXON_API_AGENT_INSTRUCTION
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
NEXON_API_KEY = os.getenv("NEXON_API_KEY")

# maplestroy character 검색 기능
def use_nexon_api(characterName : str) -> dict[str, Any]:
   """
   메이플 스토리 캐릭터의 정보 검색 기능
   사용자가 요구하는 캐릭터명을 사용하여 ocid 조회 후 캐릭터 정보를 조회
   결과를 반환한다.
   """
   headers = {
    "x-nxopen-api-key": NEXON_API_KEY
   }  
   
   url_ocid = "https://open.api.nexon.com/maplestory/v1/id"
   response = requests.get(url_ocid, params={"character_name": characterName}, headers=headers)

   if response.status_code != 200:
        return {"error": f"캐릭터 검색 실패: {response.status_code} - {response.text}"}
    
   ocid = response.json().get('ocid')

   if not ocid:
      return {"error": "캐릭터 OCID를 찾을 수 없습니다."}
   
   # ocid 기반으로 여러가지 정보 조회
   url_list = [
       f"https://open.api.nexon.com/maplestory/v1/character/basic",
       f"https://open.api.nexon.com/maplestory/v1/character/stat",
       f"https://open.api.nexon.com/maplestory/v1/character/hyper-stat",
       f"https://open.api.nexon.com/maplestory/v1/character/cashitem-equipment",
       f"https://open.api.nexon.com/maplestory/v1/character/item-equipment",
       f"https://open.api.nexon.com/maplestory/v1/character/popularity",
       f"https://open.api.nexon.com/maplestory/v1/character/dojang",
   ]

   # 응답 데이터를 저장할 딕셔너리
   data = {}

   for i, url in enumerate(url_list):
      try:
         response = requests.get(url, params={"ocid": ocid}, headers=headers)
         if response.status_code == 200 :
            # url의 엔드포인트를 키로 사용
            endpoint = url.split("/")[-1]
            # 딕셔너리에 저장
            data[endpoint] = response.json()
         else:
            data[f"error_{endpoint}"] = f"상태 코드: {response.status_code}"
      except Exception as e :
            endpoint = url.split("/")[-1]
            data[f"error_{endpoint}"] = str(e)
   
   return data            
  


# nexon_api_agent 정의
nexon_api_agent = Agent(
   name="nexon_api_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=NEXON_API_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=NEXON_API_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   tools=[use_nexon_api]
)