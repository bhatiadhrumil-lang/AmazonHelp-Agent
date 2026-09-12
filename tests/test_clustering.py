"""Tests for HDBSCAN clustering orchestration and representative selection."""
import json

import numpy as np
import pandas as pd
import pytest

from discovery.clustering import cluster_hdbscan
from discovery.cluster_analysis import intra_cluster_similarity, select_representatives
from discovery.config import HdbscanConfig


def make_blobs(n_per=40, n_blobs=3, seed=0):
    rng = np.random.default_rng(seed)
    centers = np.array([[0.0, 0.0], [8.0, 0.0], [0.0, 8.0]])
    xs = []
    for c in centers:
        xs.append(rng.normal(size=(n_per, 2)) + c)
    return np.vstack(xs)


def test_cluster_hdbscan_writes_expected_artifacts(tmp_path):
    coords_path = tmp_path / "umap_coords.npy"
    coords = make_blobs()
    np.save(coords_path, coords.astype(np.float32))

    cfg = HdbscanConfig(min_cluster_size=5, min_samples=2)
    out = cluster_hdbscan(coords_path, tmp_path / "cl", cfg)
    labels = np.load(out / "labels.npy")
    probs = np.load(out / "probabilities.npy")
    outliers = np.load(out / "outlier_scores.npy")

    assert labels.shape == (len(coords),)
    assert probs.shape == (len(coords),)
    assert outliers.shape == (len(coords),)
    assert labels.max() >= 0  # at least one real cluster
    assert (probs >= 0).all() and (probs <= 1).all()

    cfg_json = json.loads((out / "hdbscan_config.json").read_text())
    # n_clusters is the COUNT OF CLUSTERS, not the count of clustered points.
    assert cfg_json["n_clusters"] == int(labels.max()) + 1
    assert cfg_json["n_noise"] == int((labels == -1).sum())
    assert cfg_json["n_clustered_points"] == int((labels >= 0).sum())
    assert cfg_json["n_rows"] == len(coords)

    sizes = pd.read_csv(out / "cluster_size_summary.csv")
    assert len(sizes) == len(np.unique(labels))
    if (labels == -1).any():
        assert (sizes["label"] == -1).any()  # noise row present when noise exists
    assert sizes["size"].sum() == len(coords)


def test_representatives_respect_diversity(tmp_path):
    """With 8 well-separated embedding groups, reps must be one-of-each with
    cosine similarity at most the diversity cap (no top-up starvation)."""
    rng = np.random.default_rng(1)
    coords = rng.normal(size=(400, 8))
    base = rng.normal(size=(8, 8))
    base /= np.linalg.norm(base, axis=1, keepdims=True)
    # base rows are mutually -nearly-orthogonal => cosine similarity well below 0.90
    emb = np.repeat(base, 50, axis=0) + rng.normal(scale=0.02, size=(400, 8))

    reps = select_representatives(coords, emb, np.arange(400), n_rep=8, diversity_cosine=0.90)
    assert len(reps) == 8
    assert len(set(reps)) == 8
    assert all(i in range(400) for i in reps)

    from numpy.linalg import norm

    sel = emb[reps]
    seln = sel / np.maximum(norm(sel, axis=1, keepdims=True), 1e-12)
    sim = seln @ seln.T
    for i in range(len(reps)):
        for j in range(i + 1, len(reps)):
            assert sim[i, j] <= 0.90 + 0.05  # orthogonality + jitter tolerance


def test_representatives_short_cluster_returns_all():
    rng = np.random.default_rng(2)
    coords = rng.normal(size=(4, 8))
    emb = rng.normal(size=(4, 8))
    reps = select_representatives(coords, emb, np.arange(4), n_rep=8)
    assert reps == [0, 1, 2, 3]


def test_intra_cluster_similarity_nan_for_single():
    assert np.isnan(intra_cluster_similarity(np.zeros((1, 8)), np.array([0])))


def test_intra_cluster_similarity_identical_is_one():
    X = np.ones((5, 8))
    assert intra_cluster_similarity(X, np.arange(5)) == pytest.approx(1.0)