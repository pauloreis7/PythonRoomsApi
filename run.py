import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        "src.main.config.http_server_configs:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        debug=True,
    )
