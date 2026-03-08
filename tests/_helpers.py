from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_ADR = (
    REPO_ROOT
    / "tests"
    / "fixtures"
    / "ADR-0000-fixture-decision.yaml"
)


def load_module(module_name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(
        module_name,
        REPO_ROOT / relative_path,
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_example_adr() -> dict:
    with open(EXAMPLE_ADR, "r") as f:
        return copy.deepcopy(yaml.safe_load(f))


def write_yaml(path: Path, data: dict) -> Path:
    with open(path, "w") as f:
        yaml.safe_dump(data, f, sort_keys=False)
    return path
