# MedBot - AI-Powered Chat API with Memory and Document Retrieval

## Description

MedBot is an experimental microservices-based chat API project. It investigates the integration of persistent memory, document retrieval capabilities, and LLMs within a scalable containerized architecture.

## Features

- **Conversational Memory**: The API maintains context across interactions, enabling it to deliver more personalized responses.

- **Document Integration**: It uses Retrieval-Augmented Generation (RAG) techniques, the API ensures that responses are better contextualized, by providing relevant information from documents as context to the LLM using prompt engineering.

- **Microservices Architecture**: Built with modular services for flexibility and potential scalability.

## Technologies used:

- Docker
- Kubernetes
- FastAPI
- Langchain
- Postgres
- Redis
- Google Gemini APIs

## Architecture

The cluster contains a total of 5 pods, each containing specific components as follows:

- **Redis**: Utilized for storing the chat history.
- **Postgres**: Serves as a vector databas.
- **Vector Database Management Service**: Manages the addition and removal of data from the vector database.
- **Query Preprocessing Service**: Acts as the chat service's entry point. This service performs multiple functions:
   - It saves user chats to Redis.
   - Messages are then forwarded to the Question and Answer (QA) service.
   - Once the QA service returns a response, it is saved to the Redis database before being sent back as the final response to the user.
- **Question and Answer Services**: These services process the request object, which includes the query and the conversation_id. The conversation_id is used to fetch the chat history, which, along with the latest query, is used by the `ConversationalRetrievalChain`. It process retrieves relevant documents from the vector database. The documents are then used as context for the LLM. The response from the LLM is subsequently sent back to the Query Preprocessing Service.
![Architecture](https://github.com/consumer-ai-lab/microservices-based-chatbot-api/assets/93488388/465aaad8-31a1-4ca1-8136-72c6a46232db)


## Folder Structure

The project is structured as follows:

```
.
├── infra
│   └── k8s
│       ├── ingress-service.yaml
│       ├── init-sql.yaml
│       ├── postgres-manager.yaml
│       ├── query-preprocessing-manager.yaml
│       ├── question_answer_manager.yaml
│       ├── rag_uploader_manager.yaml
│       ├── redis-manager.yaml
├── query_preprocessing_service
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── redis_manager.py
├── question_answer
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── chat_manager.py
│   │   └── util.py
│   └── wait-for-postgres.sh
├── rag_uploader
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── vector_store_manager.py
│   ├── temp_data
└── skaffold.yaml
```

## Getting Started

To set up and run this project locally, follow these steps:

1. **Prerequisites:**
   - Ensure Docker and Kubernetes are installed on your system.
   - Kubernetes Ingress Controller is required for networking. It can be installed and setup with the following command:
     ```shell
     kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
     ```
2. **Set Up Skaffold:**
   - Install and configure Skaffold according to its [documentation](https://skaffold.dev/docs/).
3. **Configuration:**
   - Create a `secrets.yaml` file in the `infra/k8s` directory with your Google API key:
     ```yaml
     apiVersion: v1
     kind: Secret
     metadata:
       name: google-secret
     type: Opaque
     stringData:
       GOOGLE_API_KEY: <your-api-key>
     ```
   - Replace `my docker hub id` with your Docker Hub ID in `skaffold.yaml`, `query-preprocessing-manager.yaml`, `question_answer_manager.yaml`, and `rag_uploader_manager.yaml`. For example:
     ```yaml
     adityabhattad/query-preprocessing => <your-name>/query-processing
     ```
4. **Host File Entry:**
   - Add the following entry to your host file to route local requests:
     ```text
     127.0.0.1 medbot.xyz
     ```
5. **Start the Application:**
   - Navigate to the root directory of the project and run:
     ```shell
     skaffold dev
     ```
6. **Access the Services:**
   - The chat API can be accessed at `medbot.xyz/api/chat/docs`.
   - Document upload service is available at `medbot.xyz/api/rag/docs`.

## Note

This is an ongoing development project. Its purpose is to explore AI-powered chat API capabilities.
