"""Tests for embedding input transformation and episode loading."""
import numpy as np
import pandas as pd
import pytest

from discovery.embeddings import build_embedding_input, load_episodes


def test_strips_leading_amazonhelp():
    s = pd.Series(["@AmazonHelp my order never arrived", "@amazonhelp Help me", "No prefix here"])
    out = build_embedding_input(s)
    assert out.iloc[0] == "my order never arrived"
    assert out.iloc[1] == "Help me"
    assert out.iloc[2] == "No prefix here"


def test_keeps_mid_text_mention():
    s = pd.Series(["Can @AmazonHelp do anything about this?"])
    assert build_embedding_input(s).iloc[0] == "Can @AmazonHelp do anything about this?"


def test_html_unescape():
    s = pd.Series(["my &amp; my &lt;3 order"])
    assert build_embedding_input(s).iloc[0] == "my & my <3 order"


def test_whitespace_collapse():
    s = pd.Series(["  hello   world \n tab\there  "])
    assert build_embedding_input(s).iloc[0] == "hello world tab here"


def test_empty_and_nan():
    s = pd.Series([None, np.nan, "", "  "])
    out = build_embedding_input(s)
    assert (out == "").all()


def test_never_uses_parent_text():
    """Embedding input must be derived from customer text only; the
    metadata sidecar/input never pull AmazonHelp reply context."""
    s = pd.Series(["@AmazonHelp this is my issue"])
    out = build_embedding_input(s)
    assert "AmazonHelp" not in out.iloc[0]
    # No brand reply fields are referenced anywhere in the transform.
    import inspect

    src = inspect.getsource(build_embedding_input)
    assert "brand_parent_text" not in src
    assert "parent_id" not in src


def test_load_episodes_keeps_only_keep(tmp_path):
    df = pd.DataFrame(
        {
            "customer_message_id": [3, 1, 2],
            "conversation_id": [10, 11, 12],
            "text": ["a", "b", "c"],
            "episode_status": ["KEEP", "FLAG", "KEEP"],
        }
    )
    path = tmp_path / "ep.csv"
    df.to_csv(path, index=False)
    out = load_episodes(path, status="KEEP")
    # KEEP rows are customer_message_id {2,3}; sorted, with their own texts.
    assert list(out.customer_message_id) == [2, 3]
    assert list(out.text) == ["c", "a"]
    assert "FLAG" not in set(out.episode_status)


def test_load_episodes_missing_col(tmp_path):
    df = pd.DataFrame({"customer_message_id": [1], "text": ["a"]})
    path = tmp_path / "ep.csv"
    df.to_csv(path, index=False)
    with pytest.raises(ValueError):
        load_episodes(path)