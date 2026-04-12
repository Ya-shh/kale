# `@dsl.notebook_component` Composition Demo

Validates the **primary** Phase 4 path: wrapping real Jupyter notebooks as KFP
components via `@dsl.notebook_component` and composing them into a single
pipeline with artifacts flowing between notebook-components.

This is the exact shape the workflow compiler will produce for a
`.kale-workflow` file.

## What's in here

- `data_prep.ipynb` — tiny notebook with a `parameters`-tagged cell
  (`n_rows`, `output_path`) that writes a CSV.
- `train.ipynb` — notebook with `parameters`-tagged cell
  (`dataset_path`, `model_path`, `epochs`, `learning_rate`) that reads the
  CSV and writes a "trained model" file.
- `notebook_component_demo.py` — two `@dsl.notebook_component`s wrapping the
  notebooks, composed in an outer `@dsl.pipeline` that wires
  `data_prep → train` via a KFP `Dataset` artifact and exposes
  `n_rows` / `epochs` / `learning_rate` as pipeline parameters.
- `notebook_workflow.yaml` — compiled KFP IR (385 lines).

## Run

### Compile (produces notebook_workflow.yaml)

```bash
../../.venv/bin/python notebook_component_demo.py
# Compiled: notebook_workflow.yaml
```

### Submit to a local Kubeflow cluster

```bash
# Terminal 1: port-forward KFP API (bypasses Istio/Dex auth)
kubectl -n kubeflow port-forward svc/ml-pipeline 8888:8888

# Terminal 2: submit
../../.venv/bin/python submit.py
# → run_id: ...
# → UI URL: http://localhost:8080/_/pipeline/#/runs/details/...
```

Open the URL in a browser (logged into Kubeflow) to watch the DAG execute.
First run: 2–5 min per component (image pull + pip install of nbclient,
ipykernel, jupyter_client). Subsequent runs: under a minute total.

## Evidence in the compiled YAML

- `system.Dataset` and `system.Model` artifact schemas on the component
  interfaces.
- `NUMBER_INTEGER` / `NUMBER_DOUBLE` parameter types for `n_rows`, `epochs`,
  `learning_rate` — exposed at the outer pipeline level.
- Notebook bytes embedded inside each component's executor (Papermill-style
  parameter injection at runtime via `dsl.run_notebook(**kwargs)`).

## Why this matters

The project's goal list explicitly names **"Integrate with Kubeflow Pipelines
via `@dsl.notebook_component`."** This prototype is the minimum viable proof
that the proposed architecture works: two notebooks, one artifact connection,
runtime parameters, all compiled into a single KFP pipeline.

The earlier `kfp_nesting_demo/` prototype validates the secondary debug-mode
path (sub-pipelines with cell-level visibility). This prototype validates the
primary path. Together they cover both compilation modes described in Phase 4.
