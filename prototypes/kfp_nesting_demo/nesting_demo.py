"""
KFP v2 pipeline-in-pipeline validation prototype.

Goal: confirm that KFP v2 treats @dsl.pipeline as a first-class component
that can be nested inside another pipeline, with artifacts (Dataset, Model)
flowing cleanly between sub-pipelines.

This de-risks Phase 4 of the Composable Kale Notebooks proposal, where each
notebook compiled in debug mode becomes a sub-pipeline, and a top-level
workflow pipeline wires them together via KFP artifacts.

Run:
    uv run python nesting_demo.py
    # produces composed_workflow.yaml
"""

from kfp import compiler, dsl
from kfp.dsl import Dataset, Input, Model, Output


@dsl.component(base_image="python:3.12")
def make_dataset(out_data: Output[Dataset]) -> None:
    with open(out_data.path, "w") as f:
        f.write("x,y\n1,2\n3,4\n5,6\n")


@dsl.component(base_image="python:3.12")
def train_model(in_data: Input[Dataset], out_model: Output[Model]) -> None:
    with open(in_data.path) as f:
        rows = f.read().splitlines()[1:]
    with open(out_model.path, "w") as f:
        f.write(f"fake-model-trained-on-{len(rows)}-rows")


@dsl.component(base_image="python:3.12")
def evaluate_model(in_model: Input[Model]) -> str:
    with open(in_model.path) as f:
        return f"evaluated: {f.read()}"


@dsl.pipeline(name="data-prep-subpipeline")
def data_prep_pipeline() -> Dataset:
    step = make_dataset()
    return step.outputs["out_data"]


@dsl.pipeline(name="train-subpipeline")
def train_pipeline(dataset: Input[Dataset]) -> Model:
    step = train_model(in_data=dataset)
    return step.outputs["out_model"]


@dsl.pipeline(name="composed-workflow")
def composed_workflow() -> str:
    prep = data_prep_pipeline()
    trained = train_pipeline(dataset=prep.output)
    eval_step = evaluate_model(in_model=trained.output)
    return eval_step.output


if __name__ == "__main__":
    compiler.Compiler().compile(
        pipeline_func=composed_workflow,
        package_path="composed_workflow.yaml",
    )
    print("Compiled: composed_workflow.yaml")
