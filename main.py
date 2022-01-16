import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "factory:app",
        host="0.0.0.0",
        port=5000,
        log_level="debug",
        reload=True,
    )
