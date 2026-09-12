#!/usr/bin/env python3
"""Conversation-quality audit for the Customer Support on Twitter dataset.

Designed for the AmazonHelp take-home experiment. The script:
1. Loads TWCS from a CSV or ZIP archive.
2. Reconstructs root-based reply components using in_response_to_tweet_id.
3. Finds components containing AmazonHelp.
4. Evaluates temporal/structural quality.
5. Builds customer-problem episodes anchored on customer -> AmazonHelp interactions.
6. Writes machine-readable artifacts and a human-readable report.

No embeddings or clustering are performed here.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


EXPECTED = [
    "tweet_id", "author_id", "inbound", "created_at", "text",
    "response_tweet_id", "in_response_to_tweet_id"
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="TWCS CSV or archive.zip")
    p.add_argument("--brand", default="AmazonHelp")
    p.add_argument("--out", default="artifacts/conversation_audit")
    p.add_argument("--gap-flag-hours", type=float, default=72.0,
                   help="Flag components with an adjacent-message gap above this value")
    p.add_argument("--long-conversation-flag", type=int, default=30,
                   help="Flag components with more than this many messages")
    p.add_argument("--very-long-conversation-exclude", type=int, default=150,
                   help="Exclude components above this message count")
    p.add_argument("--min-customer-chars", type=int, default=1)
    return p.parse_args()


def open_csv(path: Path):
    if path.suffix.lower() == ".zip":
        z = zipfile.ZipFile(path)
        names = [n for n in z.namelist() if n.lower().endswith(".csv")]
        if not names:
            raise ValueError("No CSV found in ZIP archive")
        # Prefer twcs/twcs.csv when present.
        name = next((n for n in names if n.endswith("twcs/twcs.csv")), names[0])
        print(f"Reading {name} from {path}")
        return pd.read_csv(z.open(name), low_memory=False)
    return pd.read_csv(path, low_memory=False)


def normalize_id(x):
    if pd.isna(x):
        return None
    try:
        if isinstance(x, str):
            x = x.strip()
            if not x:
                return None
            if x.endswith(".0"):
                x = x[:-2]
            return int(x)
        return int(x)
    except Exception:
        return None


def clean_text(x):
    if pd.isna(x):
        return ""
    return re.sub(r"\s+", " ", str(x)).strip()


def script_flags(text: str):
    return {
        "has_cjk": bool(re.search(r"[\u3040-\u30ff\u3400-\u9fff]", text)),
        "has_devanagari": bool(re.search(r"[\u0900-\u097f]", text)),
        "has_cyrillic": bool(re.search(r"[\u0400-\u04ff]", text)),
        "has_arabic": bool(re.search(r"[\u0600-\u06ff]", text)),
        "has_thai": bool(re.search(r"[\u0e00-\u0e7f]", text)),
    }


def meaningful_customer_text(text: str, min_chars: int = 1):
    t = clean_text(text)
    if len(t) < min_chars:
        return False, "empty_or_too_short"
    # Strip common Twitter-only markers and punctuation to assess whether anything remains.
    stripped = re.sub(r"https?://\S+", " ", t)
    stripped = re.sub(r"@[A-Za-z0-9_]+", " ", stripped)
    stripped = re.sub(r"[#_]+", " ", stripped)
    stripped = re.sub(r"[^\w\u00C0-\uFFFF]+", " ", stripped, flags=re.UNICODE)
    if not stripped.strip():
        return False, "mentions_urls_only"
    return True, None


def build_root_map(df):
    """Vectorized pointer-jumping root resolution.

    Each tweet has at most one parent. Repeatedly replace parent pointers with
    grandparent pointers; after max chain rounds, every resolvable tweet points
    at its root. Missing parents are marked broken.

    Implementation note: the loop advances each pointer by ONE ancestor hop per
    iteration (not log-depth doubling), so it must run for as many rounds as the
    deepest reply chain. The dataset contains chains hundreds of tweets long, so
    the loop runs until no pointers remain active; a hard cap at n is a pure
    safety net that treats pathological cycles as broken chains.
    """
    ids = df.tweet_id.to_numpy(dtype=np.int64)
    order = np.argsort(ids)
    ids_sorted = ids[order]
    parent_series = df.parent_id.to_numpy(dtype="float64")
    parent_sorted = parent_series[order]
    # Map each parent ID to its row position in the sorted tweet IDs.
    roots = ids_sorted.copy()
    broken = np.zeros(len(ids_sorted), dtype=bool)
    # Current pointer is tweet ID. NaN means no parent/root.
    ptr = parent_sorted.copy()
    valid = ~np.isnan(ptr)
    # Parent IDs that are absent from the dataset break the chain. Anchor the
    # chain at that absent ID (consistent with how descendants resolve to it),
    # so every member of such a component shares the same root.
    if valid.any():
        pv = ptr[valid].astype(np.int64)
        pos = np.searchsorted(ids_sorted, pv)
        exists = (pos < len(ids_sorted)) & (ids_sorted[np.minimum(pos, len(ids_sorted)-1)] == pv)
        valid_idx = np.flatnonzero(valid)
        roots[valid_idx[~exists]] = pv[~exists]
        broken[valid_idx[~exists]] = True
        ptr[valid_idx[~exists]] = np.nan
        # Existing parent pointers are converted to parent IDs; pointer jumping
        # can then be performed directly using searchsorted.

    # Pointer jumping: each iteration advances every active pointer by exactly
    # one ancestor hop, so a chain of depth D needs D iterations to propagate
    # its root to all members. We therefore run until no active pointers remain.
    # The parent graph is a forest (reply chains are acyclic), so this always
    # terminates within max chain depth; the hard cap at n is a pure safety net.
    n = len(ids_sorted)
    active = ~np.isnan(ptr) & ~broken
    rounds = 0
    while active.any():
        rounds += 1
        if rounds > n:
            # Safety net for a pathological parent cycle: treat each remaining
            # active tweet as a broken root of itself (matching the naive
            # resolve() guard) rather than looping forever.
            rem_idx = np.flatnonzero(active)
            roots[rem_idx] = ids_sorted[rem_idx]
            broken[rem_idx] = True
            break
        pv = ptr[active].astype(np.int64)
        pos = np.searchsorted(ids_sorted, pv)
        exists = (pos < n) & (ids_sorted[np.minimum(pos, n-1)] == pv)
        ai = np.flatnonzero(active)
        # Missing next parent means current ptr is the last existing node's ID;
        # this is a broken chain only when the current pointer itself is absent.
        missing_next = ~exists
        if missing_next.any():
            broken[ai[missing_next]] = True
        # For existing parent, jump to its parent.
        ex_ai = ai[exists]
        ex_pos = pos[exists]
        next_ptr = parent_sorted[ex_pos]
        ptr[ex_ai] = next_ptr
        # If next_ptr is NaN, parent is the root, so resolve root to current ptr.
        root_now = np.isnan(next_ptr)
        if root_now.any():
            roots[ex_ai[root_now]] = pv[exists][root_now]
        # Keep unresolved pointers as IDs for another iteration.
        if (~root_now).any():
            roots[ex_ai[~root_now]] = next_ptr[~root_now]
        # Missing pointer: root is the current pointer, but mark broken.
        if missing_next.any():
            roots[ai[missing_next]] = pv[missing_next]
            ptr[ai[missing_next]] = np.nan
        # Stop as soon as everything has converged.
        active = ~np.isnan(ptr) & ~broken

    # For any remaining pointer, resolve by treating its current value as root.
    rem = ~np.isnan(ptr) & ~broken
    roots[rem] = ptr[rem].astype(np.int64)
    # Tweets with no parent are roots.
    no_parent = np.isnan(parent_sorted)
    roots[no_parent] = ids_sorted[no_parent]
    # Restore original row order.
    roots_out = np.empty_like(roots)
    broken_out = np.empty_like(broken)
    roots_out[order] = roots
    broken_out[order] = broken
    return roots_out, broken_out


def classify_component(group, gap_hours, long_flag, very_long_exclude, min_customer_chars):
    flags = []
    ordered = group.sort_values("created_dt")
    times = ordered.created_dt.dropna().sort_values()
    if len(times) >= 2:
        gaps = times.diff().dt.total_seconds().dropna() / 3600.0
        max_gap = float(gaps.max()) if len(gaps) else 0.0
    else:
        max_gap = 0.0
    n = len(group)
    if max_gap > gap_hours:
        flags.append("large_time_gap")
    if n > long_flag:
        flags.append("long_conversation")
    if n > very_long_exclude:
        flags.append("extreme_conversation_length")
    if group.root_broken.any():
        flags.append("broken_parent_chain")

    # A component is useful for intent discovery only if it contains at least
    # one direct customer -> brand interaction.
    direct_customer = group[(group.inbound == True) & (group.parent_author == group.brand)]
    if len(direct_customer) == 0:
        flags.append("no_direct_customer_to_brand")

    if n > very_long_exclude:
        status = "EXCLUDE"
    elif "broken_parent_chain" in flags or "no_direct_customer_to_brand" in flags:
        status = "EXCLUDE"
    elif flags:
        status = "FLAG"
    else:
        status = "KEEP"

    return status, flags, max_gap


def main():
    args = parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    df = open_csv(Path(args.input))
    missing = [c for c in EXPECTED if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df[EXPECTED].copy()
    df["tweet_id"] = pd.to_numeric(df["tweet_id"], errors="coerce").astype("Int64")
    df["parent_id"] = df["in_response_to_tweet_id"].map(normalize_id).astype("Int64")
    df["text"] = df["text"].map(clean_text)
    df["created_dt"] = pd.to_datetime(df["created_at"], format="%a %b %d %H:%M:%S %z %Y", errors="coerce", utc=True)
    df["author_id"] = df["author_id"].astype(str)
    df["inbound"] = df["inbound"].astype(bool)

    df = df[df.tweet_id.notna()].copy()
    df["tweet_id"] = df.tweet_id.astype(np.int64)
    df["parent_id"] = df.parent_id.astype("Int64")

    # Author lookup for parent -> child relationship.
    author_by_id = dict(zip(df.tweet_id, df.author_id))
    df["parent_author"] = df.parent_id.map(author_by_id)
    df["brand"] = args.brand

    print(f"Rows: {len(df):,}")
    print(f"{args.brand} tweets: {(df.author_id == args.brand).sum():,}")

    # Root-chain reconstruction.
    roots, broken = build_root_map(df)
    df["root_id"] = roots
    df["root_broken"] = broken

    brand_mask = df.author_id.eq(args.brand)
    brand_roots = set(df.loc[brand_mask, "root_id"])
    conv = df[df.root_id.isin(brand_roots)].copy()
    print(f"Brand-connected root components: {len(brand_roots):,}")

    # Component audit.
    component_rows = []
    for root_id, g in conv.groupby("root_id", sort=False):
        status, flags, max_gap = classify_component(
            g, args.gap_flag_hours, args.long_conversation_flag,
            args.very_long_conversation_exclude, args.min_customer_chars
        )
        direct_customer = g[(g.inbound == True) & (g.parent_author == args.brand)]
        component_rows.append({
            "conversation_id": int(root_id),
            "status": status,
            "flags": ";".join(flags),
            "message_count": len(g),
            "customer_messages": int((g.inbound == True).sum()),
            "brand_messages": int((g.author_id == args.brand).sum()),
            "direct_customer_to_brand": len(direct_customer),
            "unique_authors": g.author_id.nunique(),
            "start_time": g.created_dt.min(),
            "end_time": g.created_dt.max(),
            "span_hours": (g.created_dt.max() - g.created_dt.min()).total_seconds() / 3600 if g.created_dt.notna().any() else np.nan,
            "max_adjacent_gap_hours": max_gap,
        })
    components = pd.DataFrame(component_rows)
    components.to_csv(out / "conversation_components_audit.csv", index=False)

    # Build customer problem episodes from direct customer -> AmazonHelp interactions.
    direct = conv[(conv.inbound == True) & (conv.parent_author == args.brand)].copy()
    # A direct customer tweet may be a follow-up rather than an opening problem.
    # Keep it, but classify the text with conservative heuristic flags for later review.
    direct["is_acknowledgment_like"] = direct.text.str.lower().str.replace(r"[^a-z0-9 ]", " ", regex=True).str.strip().str.fullmatch(
        r"(?:thanks|thank you|thx|ty|ok|okay|yes|yep|done|got it|great|perfect|cool|sure|no problem|will do)"
    ).fillna(False)
    direct["char_len"] = direct.text.str.len()
    direct["has_url"] = direct.text.str.contains(r"https?://", regex=True, na=False)
    direct["has_brand_mention"] = direct.text.str.contains(r"@amazonhelp", case=False, regex=False, na=False)
    direct["script_cjk"] = direct.text.map(lambda x: script_flags(x)["has_cjk"])
    direct["script_devanagari"] = direct.text.map(lambda x: script_flags(x)["has_devanagari"])
    direct["script_cyrillic"] = direct.text.map(lambda x: script_flags(x)["has_cyrillic"])
    direct["script_arabic"] = direct.text.map(lambda x: script_flags(x)["has_arabic"])
    direct["script_thai"] = direct.text.map(lambda x: script_flags(x)["has_thai"])

    # Map each direct customer tweet to its root conversation and immediate parent brand text.
    brand_text = dict(zip(df.tweet_id, df.text))
    brand_time = dict(zip(df.tweet_id, df.created_dt))
    direct["brand_parent_text"] = direct.parent_id.map(brand_text).fillna("")
    direct["brand_parent_time"] = direct.parent_id.map(brand_time)
    direct["reply_gap_minutes"] = (direct.created_dt - direct.brand_parent_time).dt.total_seconds() / 60.0

    # Quality flags at episode level. We deliberately do not automatically exclude
    # multilingual or short messages; they are review signals.
    def episode_flags(r):
        flags = []
        ok, why = meaningful_customer_text(r.text, args.min_customer_chars)
        if not ok:
            flags.append(why)
        if r.is_acknowledgment_like:
            flags.append("acknowledgment_like")
        if r.char_len < 20:
            flags.append("very_short")
        if any([r.script_cjk, r.script_devanagari, r.script_cyrillic, r.script_arabic, r.script_thai]):
            flags.append("non_latin_script_signal")
        if r.reply_gap_minutes < -1:
            flags.append("customer_before_brand_parent")
        return ";".join(flags)

    direct["episode_flags"] = direct.apply(episode_flags, axis=1)
    direct["episode_status"] = np.where(
        direct.episode_flags.eq(""), "KEEP",
        np.where(direct.episode_flags.str.contains("mentions_urls_only|empty_or_too_short|customer_before_brand_parent", regex=True), "EXCLUDE", "FLAG")
    )

    episodes_cols = [
        "tweet_id", "root_id", "author_id", "created_dt", "text", "parent_id",
        "brand_parent_text", "brand_parent_time", "reply_gap_minutes", "char_len",
        "has_url", "has_brand_mention", "is_acknowledgment_like",
        "script_cjk", "script_devanagari", "script_cyrillic", "script_arabic", "script_thai",
        "episode_flags", "episode_status"
    ]
    direct[episodes_cols].rename(columns={"tweet_id": "customer_message_id", "root_id": "conversation_id"}).to_csv(
        out / "customer_problem_episodes.csv", index=False
    )

    # Build summary JSON.
    comp_counts = components.status.value_counts().to_dict()
    ep_counts = direct.episode_status.value_counts().to_dict()
    summary = {
        "brand": args.brand,
        "total_dataset_rows": int(len(df)),
        "brand_tweets": int(brand_mask.sum()),
        "brand_connected_components": int(len(brand_roots)),
        "component_status_counts": {k: int(v) for k, v in comp_counts.items()},
        "direct_customer_to_brand_episodes": int(len(direct)),
        "episode_status_counts": {k: int(v) for k, v in ep_counts.items()},
        "component_thresholds": {
            "gap_flag_hours": args.gap_flag_hours,
            "long_conversation_flag_messages": args.long_conversation_flag,
            "very_long_conversation_exclude_messages": args.very_long_conversation_exclude,
            "min_customer_chars": args.min_customer_chars,
        },
        "component_message_count_quantiles": {
            str(q): float(components.message_count.quantile(q)) for q in [0.5, 0.75, 0.9, 0.95, 0.99]
        },
        "episode_char_length_quantiles": {
            str(q): float(direct.char_len.quantile(q)) for q in [0.5, 0.75, 0.9, 0.95, 0.99]
        },
    }
    (out / "audit_summary.json").write_text(json.dumps(summary, indent=2, default=str))

    # Human-readable report.
    def pct(n, d):
        return f"{100*n/d:.2f}%" if d else "0.00%"

    lines = [
        "# AmazonHelp Conversation Quality Audit",
        "",
        f"Dataset rows: {len(df):,}",
        f"AmazonHelp tweets: {int(brand_mask.sum()):,}",
        f"AmazonHelp-connected root components: {len(brand_roots):,}",
        "",
        "## Component audit",
        "| Status | Count | Share |",
        "|---|---:|---:|",
    ]
    for s in ["KEEP", "FLAG", "EXCLUDE"]:
        n = int(comp_counts.get(s, 0))
        lines.append(f"| {s} | {n:,} | {pct(n, len(components))} |")
    lines += [
        "",
        "## Customer problem episodes",
        f"Direct customer -> {args.brand} episodes: {len(direct):,}",
        "",
        "| Status | Count | Share |",
        "|---|---:|---:|",
    ]
    for s in ["KEEP", "FLAG", "EXCLUDE"]:
        n = int(ep_counts.get(s, 0))
        lines.append(f"| {s} | {n:,} | {pct(n, len(direct))} |")
    lines += [
        "",
        "## Important methodology",
        "- Short messages, multilingual signals, URLs, and acknowledgments are not blindly deleted at the raw-data stage.",
        "- Component quality and episode quality are reported separately.",
        "- The customer problem corpus for intent discovery should use the episode table, not AmazonHelp replies as clustering text.",
        "- Historical AmazonHelp replies are retained separately for later response-evidence retrieval.",
        "- Thresholds are configurable and should be validated by manual inspection before being frozen in the report.",
    ]
    (out / "AUDIT_REPORT.md").write_text("\n".join(lines))

    print("\n=== AUDIT RESULT ===")
    print(f"Components: KEEP {comp_counts.get('KEEP',0):,} | FLAG {comp_counts.get('FLAG',0):,} | EXCLUDE {comp_counts.get('EXCLUDE',0):,}")
    print(f"Episodes:   KEEP {ep_counts.get('KEEP',0):,} | FLAG {ep_counts.get('FLAG',0):,} | EXCLUDE {ep_counts.get('EXCLUDE',0):,}")
    print(f"Artifacts written to: {out.resolve()}")


if __name__ == "__main__":
    main()