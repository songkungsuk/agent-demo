import os
from dotenv import load_dotenv
from book_agents.agent import root_agent

# 환경 변수 로드
load_dotenv()

def main():
    """메인 애플리케이션 실행 함수"""
    print("Agent Flow 애플리케이션 시작 중...")
    
    # ADK 웹 서버 시작 (FastAPI 기반)
    from google.adk import web
    web.run(root_agent, port=int(os.getenv("PORT", "8000")))

if __name__ == "__main__":
    main()