"""Tests for shared discovery configuration round-tripping."""
import json

import pytest

from discovery.config import (
    EmbeddingConfig,
    HdbscanConfig,
    UmapConfig,
    load_json,
    save_json,
)
from discovery.embeddings import asdict_cfg


def test_json_dict_roundtrip(tmp_path):
    path = tmp_path / "config.json"
    payload = {"umap": {"n_components": 8, "metric": "cosine"}, "n_rows": 100}
    save_json(path, payload)
    assert load_json(path) == payload
    assert "sort_keys" in path.read_text() or len(list(tmp_path.iterdir())) == 1


@pytest.mark.parametrize(
    "cfg",
    [EmbeddingConfig(), UmapConfig(), HdbscanConfig(), EmbeddingConfig(model="x", batch_size=16)],
)
def test_config_asdict_roundtrip(tmp_path, cfg):
    """Dataclasses are exported to plain dicts before JSON persistence."""
    data = json.loads(json.dumps(asdict_cfg(cfg)))
    save_json(tmp_path / "c.json", data)
    got = load_json(tmp_path / "c.json")
    assert got == data
    assert got.get("model") == getattr(cfg, "model", None)


def test_umap_config_defaults_locked():
    c = UmapConfig()
    assert (c.n_components, c.n_neighbors, c.metric, c.min_dist, c.random_state) == (
        8, 30, "cosine", 0.1, 42,
    )


def test_hdbscan_config_defaults_locked():
    c = HdbscanConfig()
    assert (c.min_cluster_size, c.min_samples, c.metric, c.cluster_selection_method) == (
        30, 10, "euclidean", "eom",
    )