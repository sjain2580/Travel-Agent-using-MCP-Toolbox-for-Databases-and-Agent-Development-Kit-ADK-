import os
import uvicorn
from google.adk.cli.fast_api import get_fast_api_app

# Get the ADK FastAPI app with dev UI
app = get_fast_api_app(
    agents_dir=os.path.dirname(os.path.abspath(__file__)),
    web=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
