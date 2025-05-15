from google.adk.agents import Agent
from .prompt import WEB_AGENT_DESCRIPTION, WEB_AGENT_INSTRUCTION
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import re
import html2text


def crawl_webpage_content(url: str, extract_type: str = "all") -> Dict[str, Any]:
    """웹페이지 내용을 크롤링하여 텍스트 형태로 추출합니다.
    
    주어진 URL의 웹페이지에서 텍스트 내용을 추출하고, 정제된 형태로 반환합니다.
    이 함수는 기사, 블로그 포스트, 문서 등 다양한 웹페이지의 텍스트 콘텐츠를 가져오는 데 사용됩니다.
    
    Args:
        url (str): 크롤링할 웹페이지의 URL
        extract_type (str): 추출할 내용 유형 ("all", "main_content", "title_content", "structured")
            - "all": 페이지의 모든 텍스트 내용
            - "main_content": 주요 본문 내용만 (광고, 메뉴, 헤더, 푸터 등 제외)
            - "title_content": 제목과 주요 본문 포함
            - "structured": HTML 구조를 유지한 마크다운 형식
    
    Returns:
        dict: 크롤링 결과를 포함하는 딕셔너리로 다음 키를 포함합니다.
            - status (str): "success" 또는 "error"
            - title (str): 웹페이지 제목 (성공 시)
            - content (str): 추출된 텍스트 내용 (성공 시)
            - content_type (str): 내용 유형 (성공 시)
            - metadata (dict): 추가 메타데이터 정보 (성공 시)
                - url: 원본 URL
                - word_count: 단어 수
                - estimated_read_time: 예상 읽기 시간(분)
                - main_keywords: 주요 키워드 목록
            - error_message (str): 실패 시 오류 메시지
    """
    # 입력 검증
    if not url or not url.startswith(('http://', 'https://')):
        return {
            "status": "error",
            "error_message": "유효한 URL을 입력해주세요. (http:// 또는 https://로 시작)"
        }
    
    valid_extract_types = ["all", "main_content", "title_content", "structured"]
    if extract_type not in valid_extract_types:
        return {
            "status": "error",
            "error_message": f"지원되지 않는 추출 유형입니다. 다음 중 하나를 선택하세요: {', '.join(valid_extract_types)}"
        }
    
    try:
        # 웹페이지 요청
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # HTTP 오류 검사
        
        # 응답 인코딩 처리
        if response.encoding == 'ISO-8859-1':
            response.encoding = response.apparent_encoding
        
        # BeautifulSoup으로 HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 불필요한 요소 제거
        for tag in soup(['script', 'style', 'iframe', 'nav', 'footer']):
            tag.decompose()
        
        # 페이지 제목 추출
        title = soup.title.string.strip() if soup.title else "제목 없음"
        
        # 선택된 추출 타입에 따라 내용 추출
        content = ""
        
        if extract_type == "all":
            # 모든 텍스트 추출
            content = soup.get_text(separator='\n', strip=True)
            
        elif extract_type == "main_content":
            # 주요 콘텐츠 영역 추출 시도
            main_content = None
            
            # 일반적인 메인 콘텐츠 영역 선택자
            content_selectors = [
                'article', 'main', '.content', '.post-content', '.entry-content', 
                '#content', '.article', '.post', '.entry', '.main-content'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    # 가장 큰 텍스트 영역을 가진 요소 선택
                    main_content = max(elements, key=lambda x: len(x.get_text()))
                    break
            
            # 선택자로 찾지 못한 경우 단락(p) 태그 모음으로 대체
            if not main_content:
                paragraphs = soup.find_all('p')
                # 단락이 10개 이상인 경우만 처리
                if len(paragraphs) >= 10:
                    content = '\n\n'.join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 100)
                else:
                    # 단락이 적은 경우 div 중 가장 텍스트가 많은 것 선택
                    divs = soup.find_all('div')
                    if divs:
                        main_content = max(divs, key=lambda x: len(x.get_text()))
            
            # 최종 내용 추출
            if main_content:
                content = main_content.get_text(separator='\n\n', strip=True)
        
        elif extract_type == "title_content":
            # 제목 + 주요 콘텐츠
            # 제목(h1, h2) 요소 찾기
            headers = soup.find_all(['h1', 'h2'])
            header_texts = [h.get_text().strip() for h in headers if len(h.get_text().strip()) > 10]
            
            # 주요 콘텐츠 찾기 (main_content와 동일 로직)
            main_content = None
            content_selectors = [
                'article', 'main', '.content', '.post-content', '.entry-content', 
                '#content', '.article', '.post', '.entry', '.main-content'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    main_content = max(elements, key=lambda x: len(x.get_text()))
                    break
            
            if not main_content:
                paragraphs = soup.find_all('p')
                if len(paragraphs) >= 10:
                    main_content_text = '\n\n'.join(p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 100)
                else:
                    divs = soup.find_all('div')
                    if divs:
                        main_content = max(divs, key=lambda x: len(x.get_text()))
            
            if main_content:
                main_content_text = main_content.get_text(separator='\n\n', strip=True)
            else:
                main_content_text = ""
            
            # 제목과 내용 결합
            content = '\n\n'.join(header_texts) + '\n\n' + main_content_text
            
        elif extract_type == "structured":
            # HTML을 마크다운으로 변환하여 구조 유지
            converter = html2text.HTML2Text()
            converter.ignore_links = False
            converter.ignore_images = False
            converter.ignore_tables = False
            converter.body_width = 0  # 자동 줄바꿈 비활성화
            content = converter.handle(str(soup))
        
        # 내용 정제
        # 연속된 공백과 줄바꿈 정리
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        content = content.strip()
        
        # 단어 수 계산
        word_count = len(re.findall(r'\b\w+\b', content))
        
        # 읽기 시간 추정 (평균 읽기 속도: 분당 200단어)
        read_time = max(1, round(word_count / 200))
        
        # 주요 키워드 추출 (간단한 빈도 기반)
        words = re.findall(r'\b[a-zA-Z가-힣]{2,}\b', content.lower())
        stop_words = {'및', '또는', '그리고', '하지만', '그러나', '때문에', '위해서', '통해', '이러한', '그런', '있는', '없는', 'the', 'and', 'of', 'to', 'in', 'a', 'is', 'that', 'for', 'on', 'with'}
        filtered_words = [word for word in words if word not in stop_words]
        
        word_freq = {}
        for word in filtered_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 상위 10개 키워드 추출
        keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        main_keywords = [keyword[0] for keyword in keywords]
        
        return {
            "status": "success",
            "title": title,
            "content": content,
            "content_type": extract_type,
            "metadata": {
                "url": url,
                "word_count": word_count,
                "estimated_read_time": read_time,
                "main_keywords": main_keywords
            }
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"페이지 요청 중 오류 발생: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"콘텐츠 추출 중 오류 발생: {str(e)}"
        }

# web_agent 정의
web_agent = Agent(
   name="web_agent", # 에이전트 이름
   model="gemini-2.0-flash", # 적절한 모델 선택
   description=WEB_AGENT_DESCRIPTION, # prompt.py에서 가져온 설명
   instruction=WEB_AGENT_INSTRUCTION, # prompt.py에서 가져온 지시문
   tools=[crawl_webpage_content],
)