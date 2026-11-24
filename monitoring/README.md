# Prometheus monitoring extension

The Flask application exposes Prometheus metrics at `/metrics`.

The `prometheus-config.yaml` is a configuration example, not a complete production monitoring stack. To use it:

1. Create a monitoring namespace: `kubectl create namespace monitoring`.
2. Apply the ConfigMap: `kubectl apply -f monitoring/prometheus-config.yaml`.
3. Deploy Prometheus using a maintained Helm chart or an approved operator.
4. Mount this ConfigMap into the Prometheus server and verify the target in the Prometheus UI.

For a production EKS environment, consider the Prometheus Operator / kube-prometheus-stack Helm chart and configure Grafana dashboards and alerting.
