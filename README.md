# Travel Agent — Google ADK + MCP Toolbox for Databases

An AI-powered hotel search agent built with Google Agent Development Kit (ADK) and MCP Toolbox for Databases that answers user queries about hotels in a city or by name.

Based on the Google Codelab: [Build a Travel Agent using MCP Toolbox for Databases and ADK](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk)

## Features

- Search hotels by city or location
- Search hotels by name
- Results sorted by price tier (Midscale → Luxury)
- Conversational AI powered by Gemini 2.5 Flash
- Fully serverless on Google Cloud Run

## Architecture

| Component | Technology | Role |
| ----------- | ------------ | ------ |
| **AI Agent** | Google ADK + Gemini 2.5 Flash | Understands and answers hotel queries |
| **MCP Server** | MCP Toolbox for Databases | Exposes DB as tools to the agent |
| **Database** | Cloud SQL PostgreSQL | Stores hotel data |
| **Deployment** | Google Cloud Run | Serverless hosting |

## Hotel Dataset

| Hotel | Location | Price Tier |
| ------- | ---------- | ------------ |
| Hilton Basel | Basel | Luxury |
| InterContinental Geneva | Geneva | Luxury |
| Sheraton Zurich | Zurich | Upper Upscale |
| Hyatt Regency Basel | Basel | Upper Upscale |
| Marriott Zurich | Zurich | Upscale |
| Courtyard Zurich | Zurich | Upscale |
| Best Western Bern | Bern | Upper Midscale |
| Holiday Inn Basel | Basel | Upper Midscale |
| Radisson Blu Lucerne | Lucerne | Midscale |
| Comfort Inn Bern | Bern | Midscale |

## Sample Queries

- "Which hotels are there in Basel?"
- "Tell me about the Hyatt Regency"
- "Find hotels in Zurich sorted by price"
- "Search for Marriott hotels"
- "Show me luxury hotels in Geneva"

## Prerequisites

- Google Cloud Project with billing enabled
- APIs enabled: Cloud SQL Admin, Cloud Run, Artifact Registry, Secret Manager, Vertex AI
- gcloud CLI authenticated

## Setup & Deployment

Step 1 — Create Cloud SQL Instance

```bash
gcloud sql instances create hoteldb-instance \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1 \
  --edition=ENTERPRISE \
  --root-password=postgres
```

Step 2 — Create Hotels Table & Load Data

```bash
sqlCREATE TABLE hotels(
  id INTEGER NOT NULL PRIMARY KEY, name VARCHAR NOT NULL,
  location VARCHAR NOT NULL, price_tier VARCHAR NOT NULL,
  checkin_date DATE NOT NULL, checkout_date DATE NOT NULL, booked BIT NOT NULL
);
INSERT INTO hotels VALUES
  (1,'Hilton Basel','Basel','Luxury','2024-04-20','2024-04-22',B'0'),
  (2,'Marriott Zurich','Zurich','Upscale','2024-04-14','2024-04-21',B'0'),
  (3,'Hyatt Regency Basel','Basel','Upper Upscale','2024-04-02','2024-04-20',B'0'),
  (4,'Radisson Blu Lucerne','Lucerne','Midscale','2024-04-05','2024-04-24',B'0'),
  (5,'Best Western Bern','Bern','Upper Midscale','2024-04-01','2024-04-23',B'0'),
  (6,'InterContinental Geneva','Geneva','Luxury','2024-04-23','2024-04-28',B'0'),
  (7,'Sheraton Zurich','Zurich','Upper Upscale','2024-04-02','2024-04-27',B'0'),
  (8,'Holiday Inn Basel','Basel','Upper Midscale','2024-04-09','2024-04-24',B'0'),
  (9,'Courtyard Zurich','Zurich','Upscale','2024-04-03','2024-04-13',B'0'),
  (10,'Comfort Inn Bern','Bern','Midscale','2024-04-04','2024-04-16',B'0');
```

Step 3 — Create Service Account

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
gcloud iam service-accounts create toolbox-identity
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/secretmanager.secretAccessor
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
  --role roles/cloudsql.client
```

Step 4 — Deploy MCP Toolbox

```bash
gcloud secrets create tools --data-file=tools.yaml
export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
gcloud run deploy travel-toolbox \
  --image $IMAGE --service-account toolbox-identity \
  --region us-central1 --set-secrets "/app/tools.yaml=tools:latest" \
  --args="--config=/app/tools.yaml,--address=0.0.0.0,--port=8080" \
  --allow-unauthenticated
```

Step 5 — Deploy Hotel Agent

```bash
export TOOLBOX_URL=$(gcloud run services describe travel-toolbox \
  --region=us-central1 --format="value(status.url)")
gcloud run deploy hotels-service \
  --source . --region us-central1 --allow-unauthenticated --clear-base-image \
  --set-env-vars TOOLBOX_URL=$TOOLBOX_URL,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1,GOOGLE_GENAI_USE_VERTEXAI=1
```

## Cleanup

```bash
gcloud run services delete hotels-service --region=us-central1 --quiet
gcloud run services delete travel-toolbox --region=us-central1 --quiet
gcloud sql instances delete hoteldb-instance --quiet
```

## Live Demo: [https://hotels-service-726281867698.us-central1.run.app/dev-ui/](https://hotels-service-726281867698.us-central1.run.app/dev-ui/)

## References

- Google Agent Development Kit
- MCP Toolbox for Databases
- Cloud SQL for PostgreSQL
- Original Codelab

## License

Apache License 2.0
