import azure.functions as func
import logging
import json
import re
import os
import uuid
from datetime import datetime
from azure.cosmos import CosmosClient

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


def get_container():
    connection_string = os.environ["COSMOS_CONNECTION_STRING"]
    database_name = os.environ["COSMOS_DATABASE_NAME"]
    container_name = os.environ["COSMOS_CONTAINER_NAME"]

    client = CosmosClient.from_connection_string(connection_string)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)

    return container


@app.route(route="TextAnalyzer", methods=["GET", "POST"])
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Text Analyzer API was called!")

    text = req.params.get("text")

    if not text:
        try:
            req_body = req.get_json()
            text = req_body.get("text")
        except ValueError:
            pass

    if not text:
        instructions = {
            "error": "No text provided",
            "howToUse": {
                "option1": "Add ?text=YourText to the URL",
                "option2": "Send a POST request with JSON body: {\"text\": \"Your text here\"}",
                "example": "https://your-function-url/api/TextAnalyzer?text=Hello world"
            }
        }

        return func.HttpResponse(
            json.dumps(instructions, indent=2),
            mimetype="application/json",
            status_code=400
        )

    words = text.split()
    word_count = len(words)
    char_count = len(text)
    char_count_no_spaces = len(text.replace(" ", ""))
    sentence_count = len(re.findall(r"[.!?]+", text)) or 1
    paragraph_count = len([p for p in text.split("\n\n") if p.strip()])
    reading_time_minutes = round(word_count / 200, 1)
    avg_word_length = round(char_count_no_spaces / word_count, 1) if word_count > 0 else 0
    longest_word = max(words, key=len) if words else ""

    analysis_id = str(uuid.uuid4())

    response_data = {
        "id": analysis_id,
        "analysis": {
            "wordCount": word_count,
            "characterCount": char_count,
            "characterCountNoSpaces": char_count_no_spaces,
            "sentenceCount": sentence_count,
            "paragraphCount": paragraph_count,
            "averageWordLength": avg_word_length,
            "longestWord": longest_word,
            "readingTimeMinutes": reading_time_minutes
        },
        "metadata": {
            "analyzedAt": datetime.utcnow().isoformat(),
            "textPreview": text[:100] + "..." if len(text) > 100 else text
        },
        "originalText": text
    }

    try:
        container = get_container()
        container.create_item(body=response_data)
    except Exception as e:
        logging.error(f"Error saving to Cosmos DB: {str(e)}")

        return func.HttpResponse(
            json.dumps({
                "error": "Analysis completed, but failed to save to database.",
                "details": str(e),
                "result": response_data
            }, indent=2),
            mimetype="application/json",
            status_code=500
        )

    return func.HttpResponse(
        json.dumps(response_data, indent=2),
        mimetype="application/json",
        status_code=200
    )


@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Get Analysis History API was called!")

    limit_param = req.params.get("limit")

    try:
        limit = int(limit_param) if limit_param else 10
    except ValueError:
        limit = 10

    try:
        container = get_container()

        query = f"""
        SELECT TOP {limit}
            c.id,
            c.analysis,
            c.metadata
        FROM c
        ORDER BY c.metadata.analyzedAt DESC
        """

        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))

        response_data = {
            "count": len(items),
            "results": items
        }

        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error reading from Cosmos DB: {str(e)}")

        return func.HttpResponse(
            json.dumps({
                "error": "Failed to retrieve analysis history.",
                "details": str(e)
            }, indent=2),
            mimetype="application/json",
            status_code=500
        )