# ABOUTME: The adjudicated Jev evaluation harness Plan 016 specified (Plan 017, Phase 3).
# ABOUTME: Builds the item set offline; humans label; Jev runs need the key.
"""Build and score the adjudicated Jev evaluation.

The item set samples claim-and-passage pairs from the authored records with
exact line locators. Two humans label each item (support, explicit conflict,
insufficient evidence, ambiguity) from the original evidence; Jev then answers
the same items. The report compares Jev's coarse gate against the adjudicated
labels and reports the Plan 016 go/no-go measures: material-defect recall and
alert precision. Building items is offline; labelling is human work; the live
Jev pass needs ``TYPESAFE_API_KEY``.
"""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from intake.catalog import load_build

ROOT = Path(__file__).resolve().parent.parent
LOCATOR_RE = re.compile(r"^Preserved content\.md, lines? (?P<lines>[0-9][0-9, –-]*)$", re.DOTALL)
LABELS = ("support", "explicit-conflict", "insufficient", "ambiguity")
# A material defect is an explicit conflict or an unsupported claim presented
# as established; silence alone on a properly-hedged claim is not.
MATERIAL_DEFECTS = {"explicit-conflict", "insufficient"}


@dataclass(frozen=True)
class EvalItem:
    """One claim-and-passage item with its provenance."""

    item_id: str
    record_id: str
    claim_path: str
    claim_text: str
    kind: str
    source_id: str
    passage: str
    locator: str | None
    track: str = "oracle"
    repeat_group: str | None = None

    def payload(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "record_id": self.record_id,
            "claim_path": self.claim_path,
            "claim_text": self.claim_text,
            "kind": self.kind,
            "source_id": self.source_id,
            "passage": self.passage,
            "locator": self.locator,
            "track": self.track,
            "repeat_group": self.repeat_group,
            "labels": {"labeller_a": None, "labeller_b": None, "adjudicated": None},
        }


def _locator_lines(locator: str | None) -> list[int] | None:
    if not locator:
        return None
    match = LOCATOR_RE.fullmatch(" ".join(locator.split()))
    if match is None:
        return None
    numbers = [
        int(value) for value in re.split(r"[,–-]", match.group("lines")) if value.strip().isdigit()
    ]
    return numbers or None


def _passage_for(manifest_path: str, locator: str) -> str | None:
    lines = _locator_lines(locator)
    if not lines:
        return None
    content = (ROOT / manifest_path).parent / "content.md"
    try:
        text = content.read_text(encoding="utf-8")
    except OSError:
        return None
    all_lines = text.splitlines()
    start, end = min(lines), max(lines)
    if end > len(all_lines):
        return None
    window = all_lines[start - 1 : end]
    # Widen to the surrounding paragraph so labellers see the context.
    while start > 1 and all_lines[start - 2].strip():
        start -= 1
        window.insert(0, all_lines[start - 1])
    while end < len(all_lines) and all_lines[end].strip():
        end += 1
        window.append(all_lines[end - 1])
    return "\n".join(window)


def _tokens(text: str) -> set[str]:
    """Lowercase words of length above two; a deterministic lexical unit."""
    return {word for word in re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())}


def _retrieved_passage(manifest_path: str, claim_text: str) -> str | None:
    """The capture's best paragraph for the claim, by lexical overlap.

    The retrieval track Plan 016 named: the passage is found by search, not
    by the recorded locator, so the evaluation measures the judge on the
    passages a pipeline would actually hand it. The search is deterministic
    token overlap — no embeddings; Plan 016 Design 3 stays deferred.
    """
    from intake.segment import segment_content

    content = (ROOT / manifest_path).parent / "content.md"
    try:
        text = content.read_text(encoding="utf-8")
    except OSError:
        return None
    wanted = _tokens(claim_text)
    if not wanted:
        return None
    best: tuple[int, str] | None = None
    for paragraph in segment_content(text):
        score = len(wanted & _tokens(paragraph.text))
        if score and (best is None or score > best[0]):
            best = (score, paragraph.text)
    return best[1] if best is not None else None


def build_items(
    records: list[dict[str, Any]] | None = None,
    *,
    count: int = 120,
    seed: int = 17,
    track: str = "oracle",
) -> list[dict[str, Any]]:
    """Sample claim-and-passage items from the authored records.

    The oracle track uses the passage the recorded locator names; the
    retrieval track finds the passage by lexical search, so the two measure
    the judge on located and on searched evidence respectively.
    """
    if track not in ("oracle", "retrieval"):
        raise ValueError(f"unknown track {track!r}: oracle or retrieval")
    build = load_build()
    if records is None:
        records = build.load_agents()
    candidates: list[dict[str, Any]] = []
    for record in records:
        claims = build.claim_fields(record)
        manifests = {
            source["id"]: source.get("capture", {}).get("manifest_path")
            for source in record.get("sources", [])
        }
        for path, links in record.get("evidence", {}).items():
            claim = claims.get(path)
            if claim is None:
                continue
            for link in links:
                manifest = manifests.get(link.get("source_id"))
                if not manifest:
                    continue
                if track == "oracle":
                    passage = _passage_for(manifest, link.get("locator"))
                else:
                    passage = _retrieved_passage(manifest, claim[0])
                if not passage:
                    continue
                candidates.append(
                    {
                        "record_id": record["id"],
                        "claim_path": path,
                        "claim_text": claim[0],
                        "kind": claim[1],
                        "source_id": link["source_id"],
                        "passage": passage,
                        "locator": link.get("locator"),
                    }
                )
    rng = random.Random(seed)
    rng.shuffle(candidates)
    items = []
    for index, candidate in enumerate(candidates[:count]):
        item = EvalItem(
            item_id=f"item-{index:04d}",
            record_id=candidate["record_id"],
            claim_path=candidate["claim_path"],
            claim_text=candidate["claim_text"],
            kind=candidate["kind"],
            source_id=candidate["source_id"],
            passage=candidate["passage"],
            locator=candidate["locator"],
            track=track,
        )
        items.append(item.payload())
    return items


def split_groups(
    items: list[dict[str, Any]],
    *,
    calibration_fraction: float = 0.3,
    seed: int = 17,
) -> dict[str, list[dict[str, Any]]]:
    """Split whole records into calibration and test groups.

    Grouped splits keep every item of one record on one side, so near-duplicate
    claims of the same record cannot leak across the split.
    """
    record_ids = sorted({item["record_id"] for item in items})
    rng = random.Random(seed)
    rng.shuffle(record_ids)
    cut = max(1, min(len(record_ids) - 1, round(len(record_ids) * calibration_fraction)))
    calibration_records = set(record_ids[:cut]) if len(record_ids) > 1 else set()
    calibration = [item for item in items if item["record_id"] in calibration_records]
    test = [item for item in items if item["record_id"] not in calibration_records]
    return {"calibration": calibration, "test": test}


def stress_items(
    items: list[dict[str, Any]],
    *,
    repeats: int = 2,
    seed: int = 17,
) -> list[dict[str, Any]]:
    """Repeat the items with permuted order for the stress Plan 016 named.

    Each copy carries a new item ID and the original's ``repeat_group``, so
    the stability report can see whether identical items get identical
    verdicts and whether the order changed anything.
    """
    if repeats < 1:
        raise ValueError("repeats must be at least 1")
    rng = random.Random(seed)
    stressed: list[dict[str, Any]] = []
    for copy_index in range(repeats):
        copies = []
        for item in items:
            copy = dict(item)
            copy["item_id"] = f"{item['item_id']}-r{copy_index}"
            copy["repeat_group"] = item["item_id"]
            copies.append(copy)
        rng.shuffle(copies)
        stressed.extend(copies)
    return stressed


def stability(items: list[dict[str, Any]], verdicts: dict[str, str]) -> dict[str, Any]:
    """Whether repeated copies of one item got the same verdict."""
    groups: dict[str, list[str]] = {}
    for item in items:
        group = item.get("repeat_group")
        if group and item["item_id"] in verdicts:
            groups.setdefault(group, []).append(verdicts[item["item_id"]])
    repeated = {group: outcomes for group, outcomes in groups.items() if len(outcomes) > 1}
    if not repeated:
        return {"repeated_groups": 0}
    agreeing = sum(1 for outcomes in repeated.values() if len(set(outcomes)) == 1)
    return {
        "repeated_groups": len(repeated),
        "agreeing": agreeing,
        "stability": round(agreeing / len(repeated), 4),
    }


def labeller_agreement(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Agreement between the two labellers, once both have labelled."""
    paired = [
        (item["labels"]["labeller_a"], item["labels"]["labeller_b"])
        for item in items
        if item["labels"]["labeller_a"] is not None and item["labels"]["labeller_b"] is not None
    ]
    if not paired:
        return {"labelled": 0}
    agreeing = sum(1 for a, b in paired if a == b)
    return {
        "labelled": len(paired),
        "agreeing": agreeing,
        "agreement": round(agreeing / len(paired), 4),
    }


def score(items: list[dict[str, Any]], verdicts: dict[str, str]) -> dict[str, Any]:
    """Compare the coarse gate against the adjudicated labels.

    ``verdicts`` maps item IDs to the gate's outcome: ``accept`` or ``review``.
    A material defect the gate accepted is a miss; a healthy item sent to
    review is a false alert. The Plan 016 criteria: at least 90 percent
    material-defect recall and at least 80 percent alert precision.
    """

    scored = [
        item
        for item in items
        if item["labels"]["adjudicated"] is not None and item["item_id"] in verdicts
    ]
    defects = [item for item in scored if item["labels"]["adjudicated"] in MATERIAL_DEFECTS]
    caught = sum(1 for item in defects if verdicts[item["item_id"]] == "review")
    alerts = [item for item in scored if verdicts[item["item_id"]] == "review"]
    # An alert is true when the label is anything but clean support: ambiguity
    # is also worth a person's time, so it counts as a true alert.
    true_alerts = sum(1 for item in alerts if item["labels"]["adjudicated"] != "support")
    recall = round(caught / len(defects), 4) if defects else None
    precision = round(true_alerts / len(alerts), 4) if alerts else None
    return {
        "scored": len(scored),
        "defects": len(defects),
        "defect_recall": recall,
        "alerts": len(alerts),
        "alert_precision": precision,
        "gate": {
            "material_defect_recall_min": 0.9,
            "alert_precision_min": 0.8,
            "passes": (recall is not None and recall >= 0.9)
            and (precision is None or precision >= 0.8),
        },
    }


def write_items(items: list[dict[str, Any]], path: Path) -> None:
    """Write the item set for the labellers; never overwrite an existing file."""
    if path.exists():
        raise FileExistsError(f"{path} already exists; evaluations are append-only")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_verdicts(
    items: list[dict[str, Any]],
    *,
    adapter: Any,
    budget: Any,
    cache: Any = None,
) -> dict[str, str]:
    """Ask Jev the same items and return the coarse gate's verdict per item.

    The item's passage becomes the judged state verbatim, so Jev sees exactly
    what the labellers saw. Verdicts are cached by item, passage, question
    version, and model, so a warm rerun makes no new calls.
    """

    import hashlib

    from intake.cache import cache_key, jev_cache
    from intake.judge import GATE, build_request, gates_pass, judgments_from_answers, load_questions
    from intake.models import Claim, Quote
    from intake.segment import Paragraph

    cache = cache or jev_cache()
    questions = load_questions()
    model = questions["model"]
    verdicts: dict[str, str] = {}
    for item in items:
        passage_hash = f"sha256:{hashlib.sha256(item['passage'].encode('utf-8')).hexdigest()}"
        key = cache_key(
            item["claim_text"],
            "eval",
            passage_hash,
            item["item_id"],
            str(questions.get("version", 1)),
            model,
        )
        cached = cache.get(key)
        if cached is not None:
            verdicts[item["item_id"]] = cached["verdict"]
            continue
        claim = Claim(
            id=item["item_id"],
            field="summary",
            text=item["claim_text"],
            kind=item["kind"],
            provenance="reported",
            quotes=[Quote(source=item["source_id"], text=item["claim_text"], paragraph_id="p1")],
            disposition="review",
        )
        paragraph = Paragraph(id="p1", heading_path=(), start=1, end=1, text=item["passage"])
        state, request_questions = build_request([claim], [paragraph], questions)
        result = adapter.ask(state=state, questions=request_questions, budget=budget)
        judgments = judgments_from_answers(claim, result.answers, 0, result.model)
        verdict = "accept" if gates_pass(judgments, GATE) else "review"
        verdicts[item["item_id"]] = verdict
        cache.put(key, {"verdict": verdict})
    return verdicts
