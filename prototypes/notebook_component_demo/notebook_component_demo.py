"""
@dsl.notebook_component validation prototype.

Goal: validate the PRIMARY Phase 4 path of the Composable Kale Notebooks
proposal -- wrapping real Jupyter notebooks as KFP components via
@dsl.notebook_component, then composing them into a single pipeline
with artifacts (Dataset, Model) flowing between notebook-components.

This is the exact shape of what the workflow compiler will emit for a
.kale-workflow file: one @dsl.notebook_component per notebook, wired
together in an outer @dsl.pipeline.

Run:
    .venv/bin/python notebook_component_demo.py
    # produces notebook_workflow.yaml
"""

import os

from kfp import compiler, dsl
from kfp.dsl import Dataset, Input, Model, Output

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PREP_NB = os.path.join(HERE, "data_prep.ipynb")
TRAIN_NB = os.path.join(HERE, "train.ipynb")


@dsl.notebook_component(
    notebook_path=DATA_PREP_NB,
    base_image="python:3.12",
)
def data_prep_component(
    n_rows: int,
    out_dataset: Output[Dataset],
) -> None:
    # Papermill-style parameter injection: the notebook's `parameters`-tagged
    # cell has n_rows and output_path. We override both; output_path is
    # pointed at the KFP-assigned artifact path.
    dsl.run_notebook(n_rows=n_rows, output_path=out_dataset.path)


@dsl.notebook_component(
    notebook_path=TRAIN_NB,
    base_image="python:3.12",
)
def train_component(
    in_dataset: Input[Dataset],
    epochs: int,
    learning_rate: float,
    out_model: Output[Model],
) -> None:
    dsl.run_notebook(
        dataset_path=in_dataset.path,
        model_path=out_model.path,
        epochs=epochs,
        learning_rate=learning_rate,
    )


@dsl.pipeline(name="composable-notebook-workflow")
def notebook_workflow(
    n_rows: int = 100,
    epochs: int = 10,
    learning_rate: float = 0.001,
) -> None:
    prep = data_prep_component(n_rows=n_rows)
    train_component(
        in_dataset=prep.outputs["out_dataset"],
        epochs=epochs,
        learning_rate=learning_rate,
    )


if __name__ == "__main__":
    out = os.path.join(HERE, "notebook_workflow.yaml")
    compiler.Compiler().compile(
        pipeline_func=notebook_workflow,
        package_path=out,
    )
    print(f"Compiled: {out}")
