import os
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
REQUESTS = Counter("http_requests_total", "Total HTTP requests", ["endpoint"])

@app.get("/")
def index():
    REQUESTS.labels(endpoint="/").inc()
    return jsonify(
        application="devops-demo-app",
        message="Hello from the AWS DevOps CI/CD portfolio project!",
        version=os.getenv("APP_VERSION", "1.0.0"),
        environment=os.getenv("APP_ENV", "local"),
    )

@app.get("/health")
def health():
    REQUESTS.labels(endpoint="/health").inc()
    return jsonify(status="healthy"), 200

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
