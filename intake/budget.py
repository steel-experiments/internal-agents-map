# ABOUTME: Budget reservation and run directories for the intake pipeline (Plan 017).
# ABOUTME: A run refuses to start above its reservation and stops on the first error.
"""Bound every pipeline run's cost before any model call happens.

The pattern is the Plan 016 runner's: reserve the documented worst case for
every attempted call, including failed attempts whose usage is unknown, refuse
a run whose reservation exceeds the budget passed on the command line, and
stop on the first API error. Run directories are never overwritten.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from intake.models import RunManifest, StageRun

ROOT = Path(__file__).resolve().parent.parent
RUNS_ROOT = ROOT / ".intake" / "runs"

# Published GPT-6 Sol prices at planning time, US dollars per million tokens.
DEFAULT_INPUT_PRICE_PER_MTOK = 2.0
DEFAULT_OUTPUT_PRICE_PER_MTOK = 10.0
# Conservative per-call ceilings for reservation; real calls stay far below.
DEFAULT_MAX_INPUT_TOKENS = 64_000
DEFAULT_MAX_OUTPUT_TOKENS = 16_000
# Published Jev price at planning time, with the documented maximum input
# charge reserved for every attempted request (the Plan 016 pattern).
JEV_PRICE_PER_MTOK = 0.042
JEV_MAX_REQUEST_TOKENS = 65_536
JEV_WORST_CASE_USD = JEV_MAX_REQUEST_TOKENS * JEV_PRICE_PER_MTOK / 1_000_000


class BudgetExceededError(RuntimeError):
    """The run's worst-case reservation exceeds the budget passed."""


class RunExistsError(RuntimeError):
    """A run directory already exists; runs are never overwritten."""


@dataclass
class CallReservation:
    """The worst-case cost of one model call."""

    max_input_tokens: int
    max_output_tokens: int
    input_price_per_mtok: float
    output_price_per_mtok: float

    @property
    def worst_case_usd(self) -> float:
        return (
            self.max_input_tokens * self.input_price_per_mtok
            + self.max_output_tokens * self.output_price_per_mtok
        ) / 1_000_000


def default_reservation() -> CallReservation:
    """The reservation every writer-model call reserves against."""
    return CallReservation(
        max_input_tokens=DEFAULT_MAX_INPUT_TOKENS,
        max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS,
        input_price_per_mtok=DEFAULT_INPUT_PRICE_PER_MTOK,
        output_price_per_mtok=DEFAULT_OUTPUT_PRICE_PER_MTOK,
    )


@dataclass
class Budget:
    """One run's reservation and spend ledger.

    ``reserved_usd`` holds the worst case of every planned call, reserved
    before any request happens; ``cost_usd`` holds the measured spend.
    """

    budget_usd: float
    reservation: CallReservation = field(default_factory=default_reservation)
    reserved_calls: int = 0
    reserved_usd: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0

    def _reserve(self, worst_case_usd: float, count: int, label: str) -> None:
        planned = self.reserved_usd + count * worst_case_usd
        if planned > self.budget_usd + 1e-9:
            raise BudgetExceededError(
                f"reserving {count} more {label} needs {planned:.4f} USD worst "
                f"case, above the {self.budget_usd:.4f} USD budget"
            )
        self.reserved_usd = planned
        self.reserved_calls += count

    def reserve_calls(self, count: int) -> None:
        """Reserve the worst case for a number of writer-model calls."""
        self._reserve(self.reservation.worst_case_usd, count, "writer-model calls")

    def reserve_jev_request(self, count: int = 1) -> None:
        """Reserve the worst case for Jev requests."""
        self._reserve(JEV_WORST_CASE_USD, count, "Jev requests")

    def total_reservation(self, calls: int | None = None) -> float:
        count = self.reserved_calls if calls is None else calls
        return count * self.reservation.worst_case_usd

    def record_usage(self, input_tokens: int, output_tokens: int) -> float:
        """Record one writer call's usage and return its cost."""
        cost = (
            input_tokens * self.reservation.input_price_per_mtok
            + output_tokens * self.reservation.output_price_per_mtok
        ) / 1_000_000
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.cost_usd += cost
        return cost

    def record_jev_usage(self, input_tokens: int) -> float:
        """Record one Jev request's usage and return its cost."""
        cost = input_tokens * JEV_PRICE_PER_MTOK / 1_000_000
        self.input_tokens += input_tokens
        self.cost_usd += cost
        return cost


def new_run_id(now: datetime | None = None) -> str:
    """A run ID: UTC timestamp plus four hex digits, per the model contract."""
    moment = now or datetime.now(timezone.utc)
    stamp = moment.strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{stamp}-{secrets.token_hex(2)}"


def run_directory(run_id: str, runs_root: Path = RUNS_ROOT) -> Path:
    """Create and return a fresh run directory; refuse to overwrite one."""
    directory = runs_root / run_id
    if directory.exists():
        raise RunExistsError(f"run directory {directory} already exists; never overwritten")
    directory.mkdir(parents=True)
    return directory


def write_manifest(
    directory: Path,
    *,
    run_id: str,
    queue_entry: dict[str, str | list[str]],
    stage_runs: list[StageRun],
    model_strings: dict[str, str],
    prompt_versions: dict[str, str],
    capture_hashes: dict[str, str],
    compatibility: dict[str, list[str]] | None = None,
    not_carried: dict[str, str] | None = None,
    decision: str = "needs-evidence",
    record_id: str | None = None,
    notes: list[str] | None = None,
) -> Path:
    """Write one run's manifest into its run directory."""
    manifest = RunManifest(
        run_id=run_id,
        created_at=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        queue_entry=queue_entry,
        decision=decision,  # type: ignore[arg-type]
        record_id=record_id,
        model_strings=model_strings,
        prompt_versions=prompt_versions,
        capture_hashes=capture_hashes,
        stage_runs=stage_runs,
        compatibility=compatibility or {},
        not_carried=not_carried or {},
        notes=notes or [],
    )
    path = directory / "run.json"
    path.write_text(manifest.model_dump_json(indent=2) + "\n", encoding="utf-8")
    return path
