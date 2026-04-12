"""Submit the nested-subpipeline demo to a local Kubeflow cluster.

Usage:
    kubectl -n kubeflow port-forward svc/ml-pipeline 8888:8888
    ../../.venv/bin/python submit.py
"""

from kfp.client import Client

HOST = "http://localhost:8888"
NAMESPACE = "kubeflow-user-example-com"
USER_ID = "user@example.com"
YAML = "composed_workflow.yaml"

c = Client(host=HOST, namespace=NAMESPACE)

for attr in (
    "_experiment_api",
    "_run_api",
    "_pipelines_api",
    "_job_api",
    "_upload_api",
    "_recurring_run_api",
):
    api = getattr(c, attr, None)
    if api is not None:
        api.api_client.default_headers["kubeflow-userid"] = USER_ID

c.create_experiment(name="composable-kale-nb-demo", namespace=NAMESPACE)

run = c.create_run_from_pipeline_package(
    pipeline_file=YAML,
    arguments={},
    experiment_name="composable-kale-nb-demo",
    run_name="kfp-nesting-demo-run",
    namespace=NAMESPACE,
)

print("run_id:", run.run_id)
print(f"UI URL: http://localhost:8080/_/pipeline/#/runs/details/{run.run_id}")
