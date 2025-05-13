from google.adk.agents import Agent
from book_agents.analyze_agent.agent import analyze_agent
from book_agents.agent import root_agent
from .prompt import WEB_AGENT_DESCRIPTION, WEB_AGENT_INSTRUCTION
import requests

def make_http_request(url, method='GET', params=None, data=None, headers=None, json=None, timeout=10):
    """
    HTTP 요청을 보내는 함수
    
    Parameters:
        url (str): 요청을 보낼 URL
        method (str): HTTP 메소드 (GET, POST, PUT, DELETE 등)
        params (dict): URL 쿼리 파라미터
        data (dict): 폼 데이터 또는 요청 본문
        headers (dict): HTTP 헤더
        json (dict): JSON 형식으로 보낼 데이터
        timeout (int): 요청 타임아웃 (초)
        
    Returns:
        requests.Response: 응답 객체
    """
    method = method.upper()
    
    try:
        if method == 'GET':
            response = requests.get(url, params=params, headers=headers, timeout=timeout)
        elif method == 'POST':
            response = requests.post(url, params=params, data=data, json=json, headers=headers, timeout=timeout)
        elif method == 'PUT':
            response = requests.put(url, params=params, data=data, json=json, headers=headers, timeout=timeout)
        elif method == 'DELETE':
            response = requests.delete(url, params=params, headers=headers, timeout=timeout)
        elif method == 'PATCH':
            response = requests.patch(url, params=params, data=data, json=json, headers=headers, timeout=timeout)
        else:
            raise ValueError(f"지원하지 않는 HTTP 메소드입니다: {method}")
        
        # 상태 코드 확인
        response.raise_for_status()
        return response
    
    except requests.exceptions.HTTPError as e:
        print(f"HTTP 에러 발생: {e}")
        return e.response
    except requests.exceptions.ConnectionError:
        print("연결 오류가 발생했습니다.")
        return None
    except requests.exceptions.Timeout:
        print("요청 시간이 초과되었습니다.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"요청 중 오류가 발생했습니다: {e}")
        return None


# web_agent 정의
web_agent = Agent(
   name="web_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=WEB_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=WEB_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   sub_agents=[
       analyze_agent,
       root_agent
   ],
   tools=[make_http_request],
)