이 문서는 **FastAPI 서버를 MySQL, Redis와 함께 Docker로 실행**하고,
**Python 3.12.10 로컬 개발환경**에서도 동일하게 사용할 수 있도록 구성하는 방법을 안내합니다.

---

## 🧱 아키텍처 구성

```
┌─────────────────────────────┐
│  Cursor / VSCode / Client   │
│        (LLM Agent)          │
└──────────────┬──────────────┘
               │ MCP (HTTP)
               ▼
┌─────────────────────────────┐
│     MCP Server (FastMCP)    │
│     FastAPI + MCP SDK       │
│                             │
│  ├── Tool Registry          │
│  ├── LLM Tool               │
│  └── DB Tool (optional)     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Ollama Server        │
│   (LLM Runtime, Docker)    │
└─────────────────────────────┘
```

* LLM(Client)은 **MCP HTTP API**만 호출
* FastAPI는 **Tool Router + 비즈니스 로직 분리**
* Redis는 캐시, MySQL은 영속 데이터 저장소 역할

---

## 🧱 전체 디렉토리 구조

```
mcp-llm-stack/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
└── app/
    ├── main.py              # FastMCP 엔트리
    │
    ├── mcp/
    │   ├── __init__.py
    │   └── tools.py         # MCP Tools (LLM 호출)
    │
    └── llm/
        └── ollama_client.py # Ollama 호출 로직
```

---

## 📌 VS Code 디버그 세팅

다음 파일들은 **디버그 모드 전용**입니다.

* `Dockerfile_debug`
* `docker-compose.yml_debug`

👉 VS Code에서 FastAPI + Docker + breakpoints 디버깅 가능

---

## 📌 1. 실행 방법

⚠ **Windows 환경에서는 Docker Desktop이 실행 중이어야 합니다.**

### 🐳 Docker Compose 실행

```bash
docker-compose up --build
```

### 🚀 백그라운드(데몬) 실행

```bash
docker-compose up --build -d
```

```bash
docker exec -it ollama ollama pull llama3
```

### 🛑 컨테이너 종료

```bash
docker-compose down
```

---

## 📌 Docker 캐시 제거 (빌드 오류 시)

```bash
docker build --no-cache -t myfastapi .
```

---

## 📌 Docker 캐시 충돌 오류 해결

캐시 충돌로 인해 빌드 오류가 발생할 경우 아래 명령어로 해결할 수 있습니다.

```bash
docker system prune -a
```

⚠ 실행 시 **모든 미사용 Docker 이미지/컨테이너가 제거**됩니다.

---

---
테스트 : curl -X POST "http://localhost:8000/mcp/tools/llm_chat" -H "Content-Type: application/json" --data-binary "{\"prompt\":\"What is MCP protocol?\"}"
<br>
응답 : {"prompt":"What is MCP protocol?","answer":"MCP (Multi-Chassis Link Aggregation Protocol) is a link aggregation protocol that allows multiple network
interfaces to be combined into a single, logical interface. This is useful for increasing bandwidth and improving network reliability.\n\nMCP is desig
ned to work in multi-chassis environments, where multiple devices are connected together through a common network fabric. In such environments, tradit
ional link aggregation protocols (such as LACP or PAgP) may not function correctly due to the complexity of the multi-device topology.\n\nMCP works by
 creating a virtual interface that spans across all the physical interfaces on a device. This virtual interface is then used for transmitting and rece
iving data, allowing multiple devices to be aggregated together seamlessly.\n\nSome key features of MCP include:\n\n1. Multi-chassis support: MCP allo
ws multiple devices to be connected together in a single fabric.\n2. Load balancing: MCP can distribute traffic across all the physical interfaces in
an aggregator group, improving network reliability and availability.\n3. Redundancy: MCP provides redundant links between devices, allowing for automa
tic failover in case of link failures.\n4. QoS support: MCP supports Quality of Service (QoS) policies to ensure that critical traffic is given priori
ty over non-critical traffic.\n\nMCP is an open standard protocol, and many network devices and operating systems support it. However, it's worth noti
ng that some proprietary protocols, such as Cisco's EtherChannel, may also provide similar functionality.\n\nIn summary, MCP is a link aggregation pro
tocol designed for multi-chassis environments, allowing multiple devices to be aggregated together seamlessly, improving network reliability, availabi
lity, and bandwidth."}
---

