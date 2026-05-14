"""Data Pipeline Monitor - FastAPI Backend"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Data Pipeline Monitor API",
    description="A learning project for data platform architecture",
    version="0.1.0",
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["root"])
async def root() -> dict:
    """Root endpoint - API health check."""
    return {
        "message": "Data Pipeline Monitor API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health", tags=["health"])
async def health_check() -> JSONResponse:
    """Health check endpoint for monitoring."""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "data-pipeline-monitor-api"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
