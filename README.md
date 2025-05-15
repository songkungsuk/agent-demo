# Agent-Demo

Google의 ADK(Agent Development Kit)를 활용한 에이전트 기반 시스템 데모 프로젝트입니다. 이 프로젝트는 게임 정보(메이플스토리, 리그 오브 레전드) 및 도서 정보를 제공하는 AI 에이전트 시스템을 구현합니다.

## 프로젝트 개요

이 프로젝트는 Google Gemini AI를 활용하여 멀티 에이전트 시스템을 구축했습니다. 각 에이전트는 특정 역할을 담당하고 사용자의 쿼리에 따라 적절한 하위 에이전트에 작업을 위임합니다.

### 주요 기능

- **게임 정보 제공**: 메이플스토리와 리그 오브 레전드 관련 데이터 분석 및 정보 제공
- **도서 정보 제공**: 도서 콘텐츠 분석, 웹 검색, 코딩 작업 지원

## 시스템 구조

프로젝트는 다음과 같은 두 개의 주요 에이전트 그룹으로 구성되어 있습니다:

### 1. API 에이전트 (api_agents)

- **root_agent**: 사용자 쿼리를 분석하고 적절한 하위 에이전트로 작업을 위임
- **nexon_api_agent**: 메이플스토리 캐릭터 정보를 분석하고 제공
- **riot_api_agent**: 리그 오브 레전드 게임 데이터를 분석하고 플레이어 정보 제공

### 2. 도서 에이전트 (book_agents)

- **root_agent**: 사용자 쿼리를 분석하고 적절한 하위 에이전트로 작업을 위임
- **content_analyzer**: 도서 콘텐츠 분석, 장르 분석, 테마 추출 등을 담당
- **web_agent**: 웹에서 도서 정보를 검색하고 제공
- **codinator_agent**: 복잡한 다단계 워크플로우 조정 및 여러 에이전트 간 협업 관리

## 기술 스택

- **기본 프레임워크**: FastAPI, Uvicorn
- **AI 모델**: Google Gemini AI (google-generativeai, google-adk)
- **통합 서비스**: Slack SDK, Slack Bolt
- **HTTP 통신**: Requests, HTTPX
- **환경 설정**: python-dotenv, Pydantic
- **유틸리티**: aiofiles, python-multipart

## 설치 방법

1. 저장소 클론
   ```bash
   git clone https://github.com/songkungsuk/agent-demo.git
   cd agent-demo
   ```

2. 필요한 패키지 설치
   ```bash
   pip install -r requirement.txt
   ```

3. 환경 변수 설정
   - 프로젝트 루트에 `.env` 파일을 생성하고 다음 API 키를 설정:
     ```
     NEXON_API_KEY=your_nexon_api_key
     RIOT_API_KEY=your_riot_api_key
     GOOGLE_API_KEY=your_google_api_key
     ```

## 에이전트 사용 방법

### 메이플스토리 정보 조회
메이플스토리 캐릭터에 대한 정보를 조회할 수 있습니다. `nexon_api_agent`가 다음 정보를 제공합니다:
- 기본 정보
- 스탯 정보
- 하이퍼 스탯
- 캐시 아이템 장비
- 일반 장비
- 인기도
- 무릉도장 기록

### 리그 오브 레전드 정보 조회
리그 오브 레전드 소환사에 대한 정보를 조회할 수 있습니다. `riot_api_agent`가 다음 정보를 제공합니다:
- 리그 정보
- 최근 매치 기록
- 플레이어 스타일 분석
- 게임 내용 및 흐름 분석

### 도서 정보 조회
도서 정보 시스템은 다음 기능을 제공합니다:
- 도서 콘텐츠 분석
- 도서 정보 웹 검색
- 다양한 도서 관련 작업의 조정 및 관리

## 개발 및 확장

이 프로젝트는 Google의 ADK를 활용하여 다양한 에이전트를 통합한 시스템입니다. 새로운 에이전트를 추가하거나 기존 에이전트의 기능을 확장하려면:

1. 적절한 디렉토리에 새 에이전트 폴더 생성
2. `prompt.py`에 에이전트 설명 및 지시문 정의
3. `agent.py`에 에이전트 로직 및 API 연동 코드 구현
4. 상위 `agent.py`에 새 에이전트 등록

## 라이선스

이 프로젝트는 MIT 라이선스에 따라 배포됩니다.