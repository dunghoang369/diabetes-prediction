## How-to Guide

### Traces

```shell
uvicorn trace_programmatic:app
```

#### Automatic tracing

```shell
opentelemetry-instrument --traces_exporter console --metrics_exporter none uvicorn trace_automatic:app
```

### Logs

Run ELK stack with `Filebeat`
```shell
cd elk
docker compose -f elk-docker-compose.yml -f extensions/filebeat/filebeat-compose.yml up -d
```

Quickly run a container so that `Filebeat` can collect logs from it
```shell
docker build -t foo -f logs/Dockerfile . && docker run -p 30000:30000 foo
```

### Metrics
Run the OCR app to demonstrate metrics
```shell
cd instrument/metrics
python metrics.py
```

Open another terminal to call the OCR endpoint periodically
```shell
cd instrument/metrics
python client.py
```

Now execute the following query `ocr_request_counter_total` in Prometheus at `http://localhost:9090`
