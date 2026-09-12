"""TASK 6: draw a documented, reproducible sample of HDBSCAN noise points.

Reads labels.npy + embeddings_meta.csv (row-aligned). Writes a fixed-seed
sample of noise points (labels == -1) to:
  artifacts/discovery/taxonomy/noise_sample.csv
with the full embedding_input text so the composition can be classified.

Determinism: seed fixed; sample drawn AFTER sorting by customer_message_id so
row order of meta.csv does not affect the sample.
"""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SEED = 42
N = 150

labels = np.load(ROOT / "artifacts/discovery/clustering/initial/labels.npy")
meta = pd.read_csv(ROOT / "artifacts/discovery/embeddings/full/embeddings_meta.csv",
                   keep_default_na=False)
assert len(labels) == len(meta), "label/meta length mismatch"

noise_idx = np.where(labels == -1)[0]
noise_rows = meta.iloc[noise_idx].copy()
noise_rows = noise_rows.sort_values("customer_message_id")
noise_rows = noise_rows.reset_index(drop=True)

rng = random.Random(SEED)
sample_positions = sorted(rng.sample(range(len(noise_rows)), min(N, len(noise_rows))))
sample = noise_rows.iloc[sample_positions].copy()
sample["noise_sample_pos"] = sample_positions

out_cols = ["noise_sample_pos", "customer_message_id", "conversation_id",
            "created_dt", "text", "embedding_input"]
sample[out_cols].to_csv(ROOT / "artifacts/discovery/taxonomy/noise_sample.csv",
                        index=False, encoding="utf-8")

print(f"noise points total: {len(noise_rows)}")
print(f"sample drawn: {len(sample)}  (seed={SEED}, sorted by customer_message_id)")
print(f"wrote noise_sample.csv -> {ROOT / 'artifacts/discovery/taxonomy/noise_sample.csv'}")