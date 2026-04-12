# KFP v2 Pipeline-in-Pipeline Demo

Validates Phase 4 of the Composable Kale Notebooks proposal: KFP v2 handles
nested `@dsl.pipeline` composition cleanly, with `Dataset` and `Model`
artifacts flowing between sub-pipelines.

## Run

```bash
uv pip install kfp
python nesting_demo.py
```

Produces `composed_workflow.yaml` — inspect to confirm the outer pipeline
references both sub-pipelines and wires their artifact outputs/inputs.

## Structure

- `make_dataset`, `train_model`, `evaluate_model` — leaf `@dsl.component`s.
- `data_prep_pipeline`, `train_pipeline` — inner `@dsl.pipeline`s wrapping
  those components and exposing typed artifact outputs.
- `composed_workflow` — outer `@dsl.pipeline` that calls both inner
  pipelines and wires `Dataset` → `Model` → evaluation.

This is the exact pattern the workflow compiler (Phase 4) will emit:
each notebook-in-debug-mode becomes an inner pipeline; the workflow
file becomes the outer pipeline.
