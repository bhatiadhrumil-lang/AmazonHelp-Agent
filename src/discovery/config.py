"""Shared configuration dataclasses for the intent-discovery pipeline.

Each configuration block is JSON-serializable and saved alongside its
artifacts so every experiment is self-describing and reproducible.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class EmbeddingConfig:
    backend: str = "sentence_transformers"
    model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    batch_size: int = 64
    device: str = "cpu"
    normalize: bool = True
    dtype: str = "float32"


@dataclass
class UmapConfig:
    n_components: int = 8
    n_neighbors: int = 30
    metric: str = "cosine"
    min_dist: float = 0.1
    random_state: int = 42


@dataclass
class HdbscanConfig:
    min_cluster_size: int = 30
    min_samples: int = 10
    metric: str = "euclidean"
    cluster_selection_method: str = "eom"
    prediction_data: bool = True


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def load_json(path: Path):
    return json.loads(Path(path).read_text())