# Reproducing the Three Prototypes from Scratch

Branch: `composable-kale-nb`. All paths are relative to `kale/prototypes/`.

## Prerequisites

- Docker Desktop running with Kubernetes enabled (≥ 12 GB RAM allocated)
- Local Kubeflow manifests installed in namespace `kubeflow`, user
  namespace `kubeflow-user-example-com`, user `user@example.com`
- Python venv at `kale/.venv` with `kfp==2.15.2`, `jupyterlab>=4`,
  `hatchling`, `hatch-jupyter-builder`, `editables`
- Node 18+ and `jlpm` (bundled with JupyterLab)

Verify cluster:
```bash
kubectl get nodes
kubectl -n kubeflow get deploy ml-pipeline
```

## Prototype 1 — `@dsl.notebook_component` (primary path, live run)

```bash
cd notebook_component_demo

# 1. Compile the pipeline
../../.venv/bin/python notebook_component_demo.py
# → writes notebook_workflow.yaml

# 2. Port-forward KFP API (bypasses Istio/Dex)
kubectl -n kubeflow port-forward svc/ml-pipeline 8888:8888 &

# 3. Submit to the cluster
../../.venv/bin/python submit.py
# → prints run_id and UI URL
```

UI (Istio path): `http://localhost:8080/_/pipeline/#/runs/details/<run_id>`
Or direct UI port-forward:
```bash
kubectl -n kubeflow port-forward svc/ml-pipeline-ui 8090:80 &
# → http://localhost:8090/#/runs/details/<run_id>
```

First run: 2–5 min per component (image pull + pip install).
Evidence: green DAG with `data_prep → train` via a `system.Dataset`
artifact edge and runtime parameters `n_rows`, `epochs`, `learning_rate`.

## Prototype 2 — nested sub-pipelines (debug-mode path, live run)

```bash
cd kfp_nesting_demo

# 1. Compile the pipeline
../../.venv/bin/python nesting_demo.py
# → writes composed_workflow.yaml (238 lines)

# 2. Port-forward KFP API (same as P1, skip if already running)
kubectl -n kubeflow port-forward svc/ml-pipeline 8888:8888 &

# 3. Submit to the cluster
../../.venv/bin/python submit.py
# → prints run_id and UI URL
```

Evidence: the UI shows two sub-pipelines (`data-prep-subpipeline`,
`train-subpipeline`) rendered as drill-in nodes, with `system.Dataset`
flowing from `make-dataset` into the train sub-pipeline and
`system.Model` flowing out to `evaluate-model`. Artifact schemas remain
typed across the nesting boundary.

Note: on a tightly-provisioned single-node cluster (≤ 16 GB) the
`kfp-launcher` init container can hit `Init:OOMKilled` under memory
pressure — its 128Mi limit is a hardcoded Go constant in the KFP driver.
Restarting Docker Desktop to free node memory typically clears it.

## Prototype 3 — JupyterLab workflow editor (UI path)

```bash
cd minimal-workflow-widget

# 1. Install JS deps and build the labextension
jlpm install
jlpm build

# 2. Register the Python package + labextension with JupyterLab
../../.venv/bin/python -m pip install -e .
../../.venv/bin/jupyter labextension develop . --overwrite

# 3. Launch JupyterLab
../../.venv/bin/python -c "from jupyterlab.labapp import main; main()" --port=8899
```

In the JupyterLab file browser, create a new file named `demo.kale-workflow`
(any empty file with that extension) and double-click it. A React Flow
canvas opens with three notebook nodes (`data_prep → train → evaluate`)
and typed edges. This is the shell the GSoC work will extend with
parameter forms, artifact-type validation, and compile-to-KFP actions.

## Cleaning up

```bash
# kill background port-forwards
pkill -f "port-forward svc/ml-pipeline"
```
