# MedBot - AI-Powered Chat API with Memory and Document Retrieval

## Description

MedBot is an experimental microservices-based chat API project. It explores integrating persistent memory, document retrieval capabilities, and Generative AI within a containerized architecture.

## Features

- **Conversational Memory**: The API maintains context across interactions, enabling it to deliver better responses.

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

The architecture comprises five pods, each hosting specific components:

- **Redis**: Utilized for storing the temporary chat history.
- **Postgres**: Serves as a vector database.
- **Vector Database Management Service**: Manages the addition and removal of data from the vector database.
- **Query Preprocessing Service**: Acts as the chat service's entry point. This service performs multiple functions:
   - Fetches the chat history for the ongoing session.
   - Summarizes the chat history using LLM.
   - Uses the latest query and the chat summary to generate a single consolidated query using LLM.
   - The newly generated query is then passed to **question answer service**.
   - Once the **question answer service** returns a response, the new message exchange between AI and the user is saved to redis.
   - Finally the response is returned back to the client.
- **Question and Answer Service**: When received a query from **query preprocessing service**:
   - Similarity search is performed on the query.
   - The relevant content is fetched from the vector database.
   - The document is then passed to LLM as a context with the original query, The generated response from the LLM is passed back to the **query proprocessing service**. 
![Screenshot 2024-03-03 044322](https://github.com/adityabhattad2021/microservices-based-chatbot-api/assets/93488388/b9227a71-48bf-4df8-89e8-6136cc43ac23)



## Folder Structure

The project is structured as follows:

```
├── README.md
├── infra
│   └── k8s
│       ├── ingress-service.yaml
│       ├── init-sql.yaml
│       ├── postgres-manager.yaml
│       ├── query-preprocessing-manager.yaml
│       ├── question_anwer_manager.yaml
│       ├── rag_uploader_manager.yaml
│       ├── redis-manager.yaml
│       └── secrets.yaml
├── query_preprocessing_service
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│       ├── __init__.py
│       ├── app.py
│       ├── chat_summary_manager.py
│       └── redis_manager.py
├── question_answer
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── app.py
│   │   └── query_manager.py
│   └── wait-for-postgres.sh
├── rag_uploader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── app.py
│       └── vector_store_manager.py
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
