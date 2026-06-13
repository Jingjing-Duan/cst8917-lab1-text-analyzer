# CST8917 Lab 1 - Text Analyzer with Azure Functions and Cosmos DB

## Overview

This project implements a serverless Text Analyzer API using Azure Functions and Azure Cosmos DB (Serverless).

The application analyzes text and stores analysis results in Cosmos DB. A second endpoint retrieves previously stored analysis records.

## Features

* HTTP-triggered Azure Function
* Analyze text content
* Count words, characters, sentences, and paragraphs
* Calculate average word length
* Determine the longest word
* Estimate reading time
* Store analysis results in Azure Cosmos DB
* Retrieve analysis history

## Technologies

* Python 3.12
* Azure Functions
* Azure Cosmos DB (Serverless)
* Azure Functions Core Tools
* Visual Studio Code

## API Endpoints

### TextAnalyzer

**GET**

```
/api/TextAnalyzer?text=Hello world
```

Example response:

```json
{
  "id": "...",
  "analysis": {
    "wordCount": 2
  },
  "metadata": {
    "analyzedAt": "..."
  },
  "originalText": "Hello world"
}
```

---

### GetAnalysisHistory

**GET**

```
/api/GetAnalysisHistory
```

Optional parameter:

```
/api/GetAnalysisHistory?limit=5
```

Returns previously stored analysis records from Cosmos DB.

## Environment Variables

The following settings are required:

* COSMOS_CONNECTION_STRING
* COSMOS_DATABASE_NAME
* COSMOS_CONTAINER_NAME
* AzureWebJobsStorage
* FUNCTIONS_WORKER_RUNTIME

These settings should be stored in:

* local.settings.json (local development)
* Function App Environment Variables (Azure)

## Dependencies

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

Start Azurite and run:

```bash
func start
```

## Database

* Database: TextAnalyzerDB
* Container: AnalysisResults
* Database Service: Azure Cosmos DB (Serverless)

## Author

Jingjing Duan

CST8917 - Serverless Applications

Summer 2026
