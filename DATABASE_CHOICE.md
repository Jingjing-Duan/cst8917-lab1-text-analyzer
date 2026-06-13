# DATABASE_CHOICE.md

# Database Evaluation

| Database Service             | Advantages                                                                                        | Disadvantages                                                     | Suitable for This Project |
| ---------------------------- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------- |
| Azure Cosmos DB (Serverless) | Native JSON support, flexible schema, Python SDK, scalable, easy integration with Azure Functions | Higher cost than Table Storage                                    | Yes                       |
| Azure Table Storage          | Low cost, simple key-value storage                                                                | Limited query capabilities, less flexible for JSON documents      | No                        |
| Azure SQL Database           | Powerful relational queries and transaction support                                               | Requires predefined schema, more complex setup                    | No                        |
| Azure Blob Storage           | Low cost and suitable for file storage                                                            | Not designed as a database, difficult to query historical records | No                        |

# Selected Database

Azure Cosmos DB (Serverless)

# Justification

Azure Cosmos DB (Serverless) was selected because it provides native support for JSON documents, making it ideal for storing text analysis results. It integrates easily with Azure Functions and offers strong Python SDK support. The serverless tier automatically scales based on demand and is suitable for low-traffic applications. In addition, Cosmos DB allows efficient querying when retrieving analysis history.

# Cost Considerations

Azure Cosmos DB Serverless charges based on actual usage instead of requiring dedicated throughput. This pricing model is appropriate for student projects and small workloads. Since the Text Analyzer application processes a relatively small amount of data, the overall cost is expected to remain low.
