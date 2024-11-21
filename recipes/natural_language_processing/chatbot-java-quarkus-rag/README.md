# Java-based chatbot application with SQL-based RAG - Quarkus

This application implements a chatbot with SQL RAG functionality backed by
Quarkus and its LangChain4j extension. The UI communicates with the backend
application via web sockets and the backend uses the OpenAI API to talk to
the model served by Podman AI Lab. 

The RAG data is stored in a PostgreSQL database. The application always asks
the model in the background to generate a SQL query that yields data
necessary to ask a question. Then, the application executes that query and
passes the result, encoded as a JSON object, to the model along with
the original user prompt.

Documentation for Quarkus+LangChain4j can be found at
https://docs.quarkiverse.io/quarkus-langchain4j/dev/.
