#!/usr/bin/env python3
"""
Summarize TRB gene usage for responder vs non-responder cohorts.

This utility rebuilds the patient-level table the user created in Colab by:
1. Loading the raw Sade-Feldman TCR repertoire (`sade-feldman_tcrs.csv`)
2. Attaching responder labels from `response.csv`
3. Computing counts & relative frequencies for TRB V/D/J genes
4. Optionally summarizing full VDJ combinations
5. Writing reproducible CSVs inside the repo for future runs

Example:
    python scripts/build_trb_usage_summary.py

You can override the inputs/outputs with command-line flags. Run with `-h` for details.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

import pandas as pd

# -----------------------------------------------------------------------------
# Paths
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_DATA_ROOT = (
    REPO_ROOT / "data" / "DeepTCR_Cancer-master" / "Data" / "sade-feldman"
)
DEFAULT_TCR_FILE = DEFAULT_DATA_ROOT / "sade-feldman_tcrs.csv"
DEFAULT_RESPONSE_FILE = DEFAULT_DATA_ROOT / "response.csv"
DEFAULT_OUTPUT_DIR = DEFAULT_DATA_ROOT / "processed"


# -----------------------------------------------------------------------------
# Column name helpers
# -----------------------------------------------------------------------------

TCR_COLUMN_MAP = {
    "sample_name": "sample_name",
    "beta\\delta V": "trb_v",
    "beta\\delta D": "trb_d",
    "beta\\delta J": "trb_j",
}

RESPONSE_COLUMN_MAP = {
    "Patient": "patient_id",
    "Sample name": "sample_name",
    "Response status; R-responder, NR-non-responder": "response_status",
}

STATUS_MAP = {"R": "Responder", "NR": "Non-Responder"}


# -----------------------------------------------------------------------------
# Argument parsing
# -----------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build TRB gene usage tables with counts and frequencies."
    )
    parser.add_argument(
        "--tcr-file",
        type=Path,
        default=DEFAULT_TCR_FILE,
        help=f"Path to sade-feldman TCR CSV (default: {DEFAULT_TCR_FILE})",
    )
    parser.add_argument(
        "--response-file",
        type=Path,
        default=DEFAULT_RESPONSE_FILE,
        help=f"Path to response status CSV (default: {DEFAULT_RESPONSE_FILE})",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Directory to write processed tables (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--include-vdj",
        action="store_true",
        help="Also compute full VDJ combination summaries.",
    )
    return parser.parse_args()


# -----------------------------------------------------------------------------
# Data loading & cleaning
# -----------------------------------------------------------------------------


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    copy = df.copy()
    copy.columns = [col.strip() for col in copy.columns]
    return copy


def _check_required_columns(df: pd.DataFrame, required: Iterable[str], source: Path):
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            f"File '{source}' is missing required columns: {', '.join(missing)}"
        )


def load_inputs(tcr_path: Path, response_path: Path) -> pd.DataFrame:
    if not tcr_path.exists():
        raise FileNotFoundError(f"TCR file not found: {tcr_path}")
    if not response_path.exists():
        raise FileNotFoundError(f"Response file not found: {response_path}")

    tcr_df = _normalize_columns(pd.read_csv(tcr_path))
    _check_required_columns(tcr_df, TCR_COLUMN_MAP.keys(), tcr_path)
    tcr_df = tcr_df.rename(columns=TCR_COLUMN_MAP)

    response_df = _normalize_columns(pd.read_csv(response_path))
    _check_required_columns(response_df, RESPONSE_COLUMN_MAP.keys(), response_path)
    response_df = response_df.rename(columns=RESPONSE_COLUMN_MAP)

    # Clean string columns to avoid trailing spaces from the CSV.
    for col in ("patient_id", "sample_name", "response_status"):
        response_df[col] = response_df[col].astype(str).str.strip()
    response_df["response_status"] = response_df["response_status"].str.upper()
    response_df["response_status"] = response_df["response_status"].map(
        lambda code: STATUS_MAP.get(code, code)
    )
    response_df = response_df.drop_duplicates(subset="sample_name", keep="first")

    for col in ("sample_name",):
        tcr_df[col] = tcr_df[col].astype(str).str.strip()

    merged = pd.merge(
        tcr_df,
        response_df,
        on="sample_name",
        how="inner",
        validate="many_to_one",
        sort=False,
    )

    if merged.empty:
        raise ValueError(
            "Merging TCR data with response labels produced 0 rows. "
            "Check that sample_name values overlap."
        )

    merged["patient_id"] = merged["patient_id"].astype(str).str.strip()
    merged["response_status"] = merged["response_status"].fillna("Unknown")
    return merged


# -----------------------------------------------------------------------------
# Summaries
# -----------------------------------------------------------------------------


def _format_frequency(series: pd.Series) -> pd.Series:
    return (series.astype(float)).round(6)


def summarize_gene_usage(
    df: pd.DataFrame, group_cols: List[str], gene_col: str, gene_label: str
) -> pd.DataFrame:
    non_null = df.dropna(subset=[gene_col])
    if non_null.empty:
        return pd.DataFrame(
            columns=group_cols
            + ["gene_type", "gene", "count", "total_sequences", "frequency"]
        )

    counts = (
        non_null.groupby(group_cols + [gene_col], dropna=False)
        .size()
        .reset_index(name="count")
    )
    counts = counts.rename(columns={gene_col: "gene"})
    counts["total_sequences"] = counts.groupby(group_cols)["count"].transform("sum")
    counts["count"] = counts["count"].astype(int)
    counts["total_sequences"] = counts["total_sequences"].astype(int)
    counts["frequency"] = counts["count"] / counts["total_sequences"]
    counts["frequency"] = _format_frequency(counts["frequency"])
    counts["gene_type"] = gene_label
    counts = counts[
        group_cols + ["gene_type", "gene", "count", "total_sequences", "frequency"]
    ]
    sort_cols = group_cols + ["gene_type", "count", "gene"]
    ascending = [True] * len(group_cols) + [True, False, True]
    counts = counts.sort_values(sort_cols, ascending=ascending).reset_index(drop=True)
    return counts


def summarize_vdj_usage(df: pd.DataFrame, group_cols: List[str]) -> pd.DataFrame:
    non_null = df.dropna(subset=["trb_v", "trb_d", "trb_j"])
    if non_null.empty:
        return pd.DataFrame(
            columns=group_cols
            + ["v_gene", "d_gene", "j_gene", "count", "total_sequences", "frequency"]
        )

    counts = (
        non_null.groupby(group_cols + ["trb_v", "trb_d", "trb_j"], dropna=False)
        .size()
        .reset_index(name="count")
    )
    counts["total_sequences"] = counts.groupby(group_cols)["count"].transform("sum")
    counts["count"] = counts["count"].astype(int)
    counts["total_sequences"] = counts["total_sequences"].astype(int)
    counts["frequency"] = _format_frequency(counts["count"] / counts["total_sequences"])
    counts = counts.rename(
        columns={"trb_v": "v_gene", "trb_d": "d_gene", "trb_j": "j_gene"}
    )
    counts = counts[
        group_cols + ["v_gene", "d_gene", "j_gene", "count", "total_sequences", "frequency"]
    ]
    sort_cols = group_cols + ["count", "v_gene", "d_gene", "j_gene"]
    ascending = [True] * len(group_cols) + [False, True, True, True]
    counts = counts.sort_values(sort_cols, ascending=ascending).reset_index(drop=True)
    return counts


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def main():
    args = parse_args()

    merged = load_inputs(args.tcr_file, args.response_file)
    group_by_sample = ["patient_id", "sample_name", "response_status"]
    group_by_patient = ["patient_id", "response_status"]

    gene_tables = []
    for gene_col, label in (("trb_v", "TRBV"), ("trb_d", "TRBD"), ("trb_j", "TRBJ")):
        gene_tables.append(
            summarize_gene_usage(merged, group_by_sample, gene_col, label)
        )
    gene_usage_by_sample = pd.concat(gene_tables, ignore_index=True)
    patient_gene_tables = []
    for gene_col, label in (("trb_v", "TRBV"), ("trb_d", "TRBD"), ("trb_j", "TRBJ")):
        patient_gene_tables.append(
            summarize_gene_usage(merged, group_by_patient, gene_col, label)
        )
    gene_usage_by_patient = pd.concat(patient_gene_tables, ignore_index=True)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    sample_gene_path = args.output_dir / "trb_gene_usage_by_sample.csv"
    patient_gene_path = args.output_dir / "trb_gene_usage_by_patient.csv"

    gene_usage_by_sample.to_csv(sample_gene_path, index=False)
    gene_usage_by_patient.to_csv(patient_gene_path, index=False)

    print(f"Wrote {len(gene_usage_by_sample):,} rows -> {sample_gene_path}")
    print(f"Wrote {len(gene_usage_by_patient):,} rows -> {patient_gene_path}")

    if args.include_vdj:
        vdj_by_sample = summarize_vdj_usage(merged, group_by_sample)
        vdj_by_patient = summarize_vdj_usage(merged, group_by_patient)

        vdj_sample_path = args.output_dir / "trb_vdj_usage_by_sample.csv"
        vdj_patient_path = args.output_dir / "trb_vdj_usage_by_patient.csv"

        vdj_by_sample.to_csv(vdj_sample_path, index=False)
        vdj_by_patient.to_csv(vdj_patient_path, index=False)

        print(f"Wrote {len(vdj_by_sample):,} rows -> {vdj_sample_path}")
        print(f"Wrote {len(vdj_by_patient):,} rows -> {vdj_patient_path}")


if __name__ == "__main__":
    main()
