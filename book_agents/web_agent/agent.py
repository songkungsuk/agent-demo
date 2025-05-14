from google.adk.agents import Agent
from .prompt import WEB_AGENT_DESCRIPTION, WEB_AGENT_INSTRUCTION
import requests
from bs4 import BeautifulSoup

def crawl_url(url: str) -> dict:
    """
    A simple function to crawl a URL and return HTML content
    
    Parameters:
    - url (str): URL of the webpage to crawl
    
    Returns:
    - dict: Dictionary containing HTML content and status
    - None: If an error occurs
    """
    try:
        # 기본 헤더 설정
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # HTTP GET 요청 보내기
        response = requests.get(url, headers=headers, timeout=10)
        
        # 응답 상태 코드 확인
        response.raise_for_status()
        
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        today_area = soup.find('div', id='yTodayBSet')
        
        # BeautifulSoup Tag 객체를 직렬화 가능한 형태로 변환
        if today_area:
            return {
                'status': 'success',
                'content': str(today_area),  # Tag 객체를 문자열로 변환
                'url': url
            }
        else:
            return {
                'status': 'not_found',
                'message': 'Target element not found',
                'url': url
            }
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return {
            'status': 'error',
            'error_message': str(e),
            'url': url
        }

# web_agent 정의
web_agent = Agent(
   name="web_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=WEB_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=WEB_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   tools=[crawl_url],
)