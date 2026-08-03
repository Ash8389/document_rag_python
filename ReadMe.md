<div align="center">

# 📄 Document RAG (Python)

### Chat with your PDFs — powered by a real event-driven microservices pipeline.

**Upload → Chunk → Embed → Store → Retrieve → Rerank → Answer**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-async-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Kafka](https://img.shields.io/badge/Kafka-KRaft-231F20?logo=apachekafka&logoColor=white)](https://kafka.apache.org/)
[![Qdrant](https://img.shields.io/badge/Qdrant-vector--db-DC244C)](https://qdrant.tech/)
[![Redis](https://img.shields.io/badge/Redis-cache%20%2B%20memory-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-compose-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

## ✨ Why this project?

Most RAG demos are a single notebook. This one is built the way a **production system** actually looks — three independent, containerized services talking to each other over **Kafka**, with a vector store, a cache, and an LLM in the loop. If you want to learn how a real RAG backend is architected (not just "call an embedding API in a for-loop"), this repo is a great blueprint.

```
   PDF Upload                 Kafka Topic                  Vector Search + LLM
┌────────────────┐        ┌──────────────────┐        ┌──────────────────────────┐
│  Ingestion      │──────▶│  document.chunks │──────▶│  Embedding   │  Query      │
│  Service (8081) │        │   (3 partitions) │        │  Service(8082)│Service(8083)│
└────────────────┘        └──────────────────┘        └──────────────────────────┘
                                                              │           │
                                                          Qdrant       Redis + Groq LLM
                                                        (vectors)    (cache/history/answer)
```

---

## 🧩 The Pipeline, Step by Step

| Stage | Service | What happens |
|---|---|---|
| 1️⃣ **Upload** | `ingestion_service` | You `POST` a PDF. It's saved to disk and parsed with **PyMuPDF**. |
| 2️⃣ **Clean** | `ingestion_service` | Unicode normalization, whitespace/newline cleanup. |
| 3️⃣ **Chunk** | `ingestion_service` | Split into 500-char chunks (75-char overlap) via LangChain's `RecursiveCharacterTextSplitter`. |
| 4️⃣ **Enrich** | `ingestion_service` | Each chunk gets a UUID, chunk index, language tag, and correct page number. |
| 5️⃣ **Publish** | `ingestion_service` → Kafka | Chunks streamed to the `document.chunks` topic; an `END` marker signals "batch done." |
| 6️⃣ **Embed** | `embedding_service` | Consumes chunks in batches of 10, embeds them with **Jina embeddings**, upserts into **Qdrant**. |
| 7️⃣ **Ask** | `query_service` | Checks **Redis cache** first — instant answer if the question was asked before. |
| 8️⃣ **Retrieve** | `query_service` | Embeds your question, does a **top-10 similarity search** in Qdrant. |
| 9️⃣ **Rerank** | `query_service` | **Cohere `rerank-v3.5`** trims the top 10 down to the 3 most relevant chunks. |
| 🔟 **Answer** | `query_service` | The best chunks + conversation history are sent to an LLM via **Groq**, response is cached, and chat history is persisted in Redis. |

---

## 🏗️ Architecture

```
                         ┌────────────┐
                         │  Traefik   │  ← API Gateway
                         │  Gateway   │
                         └─────┬──────┘
                    ┌──────────┴──────────┐
              /ingest│                    │/chat
                     ▼                    ▼
           ┌──────────────────┐   ┌──────────────────┐
           │ Ingestion Service│   │  Query Service    │
           │      :8081       │   │      :8083        │
           └────────┬─────────┘   └───┬───────┬───────┘
                    │                 │       │
                    ▼                 ▼       ▼
              ┌───────────┐     ┌─────────┐ ┌───────┐
              │   Kafka   │     │ Qdrant  │ │ Redis │
              └─────┬─────┘     └────▲────┘ └───────┘
                    │                │
                    ▼                │
           ┌──────────────────┐      │
           │ Embedding Service│──────┘
           │      :8082       │
           └──────────────────┘
```

**Services:**
- 🟢 **`ingestion_service`** — PDF upload, cleaning, chunking, publishing to Kafka
- 🔵 **`embedding_service`** — Kafka consumer, Jina embeddings, Qdrant writer
- 🟣 **`query_service`** — retrieval, Cohere reranking, Groq LLM chat, Redis cache & memory

**Infra:**
- **Kafka** (KRaft mode — no Zookeeper needed) — decouples ingestion from embedding
- **Qdrant** — vector similarity search (cosine distance)
- **Redis Stack** — answer caching + per-session chat history (last 10 messages, 1hr TTL)
- **Traefik** — routes `/ingest → 8081` and `/chat → 8083`

---

## 🚀 Quick Start

### 1. Clone & configure
```bash
git clone https://github.com/Ash8389/document_rag_python.git
cd document_rag_python
```

Each service needs its own `.env` file. Create these before running:

**`embedding_service/.env`**
```env
JINA_API_KEY=your_jina_key
JINA_BASE_URL=https://api.jina.ai/v1
JINA_MODEL=jina-embeddings-v3
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
EMBEDDING_DIMENSION=1024
```

**`query_service/.env`**
```env
JINA_API_KEY=your_jina_key
JINA_BASE_URL=https://api.jina.ai/v1
JINA_MODEL=jina-embeddings-v3
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=documents
EMBEDDING_DIMENSION=1024

GROQ_API_KEY=your_groq_key
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_CHAT_MODEL=llama-3.3-70b-versatile

COHERE_API_KEY=your_cohere_key

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_TTL_MIN=3600
```

### 2. Spin everything up
```bash
docker compose up --build
```

This launches Kafka, Qdrant, Redis, Traefik, and all three services.

### 3. Ingest a PDF
```bash
curl -X POST http://localhost/ingest/pdf \
  -F "file=@attention_all_you_need.pdf"
```

### 4. Ask a question 🎉
```bash
curl "http://localhost/chat?question=What is the transformer architecture?"
```

```json
{
  "answer": "The Transformer is a model architecture that relies entirely on an attention mechanism...",
  "model_name": "llama-3.3-70b-versatile",
  "input_tokens": 512,
  "output_tokens": 128,
  "total_tokens": 640
}
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI (async) |
| Message Broker | Apache Kafka (KRaft) via `aiokafka` |
| Vector Database | Qdrant |
| Cache & Chat Memory | Redis Stack |
| Embeddings | Jina Embeddings (OpenAI-compatible API) |
| Reranking | Cohere `rerank-v3.5` |
| LLM | Groq (OpenAI-compatible API) |
| Orchestration | LangChain (loaders, splitters, chains) |
| Gateway | Traefik |
| Containerization | Docker Compose |

---

## 📂 Project Structure

```
document_rag_python/
├── ingestion_service/       # PDF upload → clean → chunk → publish to Kafka
│   └── app/
│       ├── loaders/         # PyMuPDF PDF loader
│       ├── processors/      # cleaner, chunker, metadata enrichment
│       ├── kafka/           # producer + topic setup
│       └── routes/          # POST /ingest/pdf
│
├── embedding_service/       # Kafka consumer → embed → store in Qdrant
│   └── app/
│       ├── kafka/           # consumer
│       ├── processors/      # Jina embedding calls
│       └── qdrant/          # collection creation + upsert
│
├── query_service/           # retrieve → rerank → chat → cache
│   └── app/
│       ├── repo/            # VectorRepository abstraction (Qdrant impl)
│       ├── reranker/        # Cohere reranking
│       ├── chat/            # ChatModel abstraction (Groq/OpenAI impl)
│       ├── redis/           # cache + chat history
│       └── routes/          # GET /chat
│
└── docker-compose.yml       # Kafka, Qdrant, Redis, Traefik, all 3 services
```

---

## 🎯 Design Highlights

- **Event-driven ingestion** — Kafka decouples PDF parsing from embedding, so large documents don't block the upload request.
- **Pluggable abstractions** — `VectorRepository` and `ChatModel` are abstract base classes, so swapping Qdrant → Pinecone or Groq → OpenAI is a one-file change.
- **Cache-first querying** — repeated questions are served instantly from Redis without touching the vector DB or LLM.
- **Persistent conversation memory** — chat history lives in Redis per session, capped to the last 10 messages.

---

## 🗺️ Roadmap Ideas

- [ ] Add automated tests
- [ ] Support multi-file / multi-format ingestion (docx, txt, html)
- [ ] Add a lightweight frontend for uploads & chat
- [ ] Streaming responses from the LLM
- [ ] Auth on the Traefik gateway

---

<div align="center">

**Built with FastAPI, Kafka, Qdrant, Redis, Cohere & Groq**

⭐ If you find this architecture useful, consider starring the repo!

</div>