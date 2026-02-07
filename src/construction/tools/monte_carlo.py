"""Monte Carlo schedule simulation tool using NumPy."""

import json
from datetime import UTC, date, datetime, timedelta

import numpy as np

from ai_agent.tools import Tool

# Default baseline activities with triangular distribution params
# Each: (name, min_days, mode_days, max_days, is_critical)
_DEFAULT_ACTIVITIES = [
    ("Foundation Pour", 10, 14, 21, True),
    ("Steel Erection", 25, 30, 40, True),
    ("MEP Rough-In", 20, 30, 45, True),
    ("Cooling Loop Install", 25, 30, 38, True),
    ("Exterior Envelope", 15, 20, 30, False),
    ("Interior Finishes", 20, 25, 35, False),
    ("Commissioning", 10, 14, 21, True),
]


class MonteCarloSimulationTool(Tool):
    """Run Monte Carlo simulation on project schedule."""

    name = "monte_carlo_simulation"
    description = (
        "Run Monte Carlo simulation on project schedule"
        " to estimate completion probability."
    )

    def get_input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "The project identifier.",
                },
                "iterations": {
                    "type": "integer",
                    "description": (
                        "Number of simulation iterations."
                    ),
                    "default": 10000,
                },
                "activity_durations": {
                    "type": "object",
                    "description": (
                        "Override activity durations as"
                        " {name: {min, mode, max}}."
                    ),
                },
                "confidence_levels": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": (
                        "Percentiles to report, e.g."
                        " [0.5, 0.8, 0.95]."
                    ),
                    "default": [0.5, 0.8, 0.95],
                },
            },
            "required": ["project_id"],
        }

    def execute(self, **kwargs) -> str:
        project_id = kwargs["project_id"]
        iterations = kwargs.get("iterations", 10000)
        overrides = kwargs.get("activity_durations") or {}
        confidence_levels = kwargs.get(
            "confidence_levels", [0.5, 0.8, 0.95]
        )

        try:
            return self._run_simulation(
                project_id,
                iterations,
                overrides,
                confidence_levels,
            )
        except Exception as exc:
            return f"Error: {exc}"

    def _run_simulation(
        self,
        project_id: str,
        iterations: int,
        overrides: dict,
        confidence_levels: list[float],
    ) -> str:
        rng = np.random.default_rng()
        today = date.today()

        # Build activity list with distribution params
        activities = []
        for name, min_d, mode_d, max_d, critical in _DEFAULT_ACTIVITIES:
            if name in overrides:
                ov = overrides[name]
                min_d = ov.get("min", min_d)
                mode_d = ov.get("mode", mode_d)
                max_d = ov.get("max", max_d)
            activities.append((name, min_d, mode_d, max_d, critical))

        # Simulate: critical path is sum of critical activities
        critical_activities = [
            a for a in activities if a[4]
        ]
        all_activities = activities

        # Sample durations for each critical activity
        critical_durations = np.zeros(iterations)
        float_consumed_samples: dict[str, np.ndarray] = {}

        for name, min_d, mode_d, max_d, _ in critical_activities:
            samples = rng.triangular(
                min_d, mode_d, max_d, size=iterations
            )
            critical_durations += samples
            # Float consumed = actual - mode (baseline)
            float_consumed_samples[name] = samples - mode_d

        # Non-critical float consumption
        for name, min_d, mode_d, max_d, is_crit in all_activities:
            if not is_crit:
                samples = rng.triangular(
                    min_d, mode_d, max_d, size=iterations
                )
                float_consumed_samples[name] = samples - mode_d

        # Calculate percentiles
        percentile_values = np.percentile(
            critical_durations,
            [lvl * 100 for lvl in confidence_levels],
        )

        completion_dates = {}
        for lvl, val in zip(
            confidence_levels, percentile_values, strict=False
        ):
            key = f"p{int(lvl * 100)}"
            completion_dates[key] = (
                today + timedelta(days=int(val))
            ).isoformat()

        # Average float consumed per activity
        float_consumed = {
            name: round(float(np.mean(samples)), 2)
            for name, samples in float_consumed_samples.items()
        }

        # Build histogram (10 bins)
        hist_counts, hist_edges = np.histogram(
            critical_durations, bins=10
        )
        histogram = []
        for i, count in enumerate(hist_counts):
            histogram.append({
                "bin_start": round(float(hist_edges[i]), 1),
                "bin_end": round(float(hist_edges[i + 1]), 1),
                "count": int(count),
            })

        # Confidence: fraction within baseline total
        baseline_total = sum(
            a[2] for a in critical_activities
        )
        confidence = float(
            np.mean(critical_durations <= baseline_total)
        )

        result = {
            "project_id": project_id,
            "iterations": iterations,
            "p50_completion": completion_dates.get(
                "p50", completion_dates.get(
                    next(iter(completion_dates.keys()))
                )
            ),
            "p80_completion": completion_dates.get(
                "p80", ""
            ),
            "p95_completion": completion_dates.get(
                "p95", ""
            ),
            "confidence": round(confidence, 4),
            "float_consumed": float_consumed,
            "histogram": histogram,
            "run_at": datetime.now(UTC).isoformat(),
        }
        return json.dumps(result, indent=2)
