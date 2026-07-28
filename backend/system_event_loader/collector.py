from prometheus_client import start_http_server, Counter, Gauge
import time

# 1. Definir les metrics dialk
REQUEST_COUNT = Counter('system_event_requests_total', 'Total system events processed')
CPU_GAUGE = Gauge('system_cpu_usage_percent', 'Current CPU usage percentage')

# 2. Dmarr l-server dial Prometheus metrics f port 8000
start_http_server(8000)
print("Prometheus metrics server running on port 8000...")

# Example usage f l-loop dialk:
# REQUEST_COUNT.inc()
# CPU_GAUGE.set(45.2)