# Minimal Workflow Widget (Prototype)

De-risks Phase 5 of the Composable Kale Notebooks proposal. Proves three things:

1. JupyterLab's `DocumentRegistry` accepts a custom `.demo-workflow` file type.
2. A `DocumentWidget` can host a React tree via `ReactWidget`.
3. React Flow renders inside a Lumino widget without layout or styling conflicts.

## Build & run

```bash
cd prototypes/minimal-workflow-widget
jlpm install
jlpm run build
jupyter labextension develop . --overwrite
jupyter lab
```

Then in the file browser, double-click `example.demo-workflow`. The editor opens
with three notebook nodes (`data_prep.ipynb → train.ipynb → evaluate.ipynb`)
connected by typed edges (`Dataset`, `Model`), plus pan/zoom controls and a
mini-map.

## What's intentionally NOT here

- Saving/loading canvas state back to the file (Phase 5 scope).
- Dragging notebooks from the file browser onto the canvas (Phase 5 scope).
- RPC to the backend (Phase 6 scope).
- Port-level edge validation (Phase 5 scope).

This is a viability check, not a partial implementation.

## Files

- `src/index.ts` — registers the file type and `WidgetFactory`.
- `src/WorkflowWidget.tsx` — `ReactWidget` hosting React Flow with a hard-coded
  three-node demo graph.
- `example.demo-workflow` — empty JSON file to double-click.
