from __future__ import annotations

import json
from decimal import Decimal

from evaluation.chatbot.evaluate_extraction_accuracy import (
    build_run_id,
    canonicalize_result,
    compare_results,
    resolve_run_paths,
    summarize,
)


def test_alias_only_difference_is_match():
    result = compare_results(
        ["total_internacoes"],
        [(10,)],
        ["total"],
        [(10,)],
        mode="scalar",
    )

    assert result.result_match is True
    assert result.alias_only_difference is True
    assert result.error_category is None


def test_value_mismatch_is_not_match():
    result = compare_results(
        ["total"],
        [(10,)],
        ["total"],
        [(11,)],
        mode="scalar",
    )

    assert result.result_match is False
    assert result.error_category == "value_mismatch"


def test_shape_mismatch_is_not_match():
    result = compare_results(
        ["uf", "total"],
        [("MA", 10)],
        ["uf"],
        [("MA",)],
        mode="ordered",
    )

    assert result.result_match is False
    assert result.shape_match is False
    assert result.error_category == "shape_mismatch"


def test_unordered_distribution_matches_same_rows_different_order():
    result = compare_results(
        ["uf", "total"],
        [("MA", 1), ("RS", 2)],
        ["uf", "total"],
        [("RS", 2), ("MA", 1)],
        mode="unordered",
    )

    assert result.result_match is True
    assert result.order_only_mismatch is False


def test_ordered_mode_reports_order_only_mismatch():
    result = compare_results(
        ["uf", "total"],
        [("MA", 1), ("RS", 2)],
        ["uf", "total"],
        [("RS", 2), ("MA", 1)],
        mode="ordered",
    )

    assert result.result_match is False
    assert result.order_only_mismatch is True
    assert result.error_category == "order_only_mismatch"


def test_numeric_tolerance_accepts_small_decimal_difference():
    result = compare_results(
        ["taxa"],
        [(Decimal("10.0000001"),)],
        ["taxa"],
        [(10.0000002,)],
        mode="scalar",
        numeric_tolerance=1e-6,
    )

    assert result.result_match is True


def test_numeric_text_matches_number_as_type_only_difference():
    result = compare_results(
        ["ano", "total"],
        [(2000, 9)],
        ["ano_entrada", "total"],
        [("2000", 9)],
        mode="ordered",
    )

    assert result.result_match is True
    assert result.alias_only_difference is True
    assert result.type_only_difference is True


def test_canonicalize_result_ignores_column_names_and_normalizes_decimal():
    expected = canonicalize_result(["alias_a"], [(Decimal("10.50"),)])
    actual = canonicalize_result(["alias_b"], [(10.5,)])

    assert expected == actual


def test_summary_is_json_serializable_and_counts_categories():
    records = [
        {
            "intent_status": "answerable",
            "generated_sql": "SELECT 1",
            "generated_sql_valid": True,
            "generated_execution_status": "passed",
            "ground_truth_execution_status": "passed",
            "expected_truncated": False,
            "actual_truncated": False,
            "result_match": True,
            "alias_only_difference": True,
            "type_only_difference": False,
            "order_only_mismatch": False,
            "error_category": None,
        },
        {
            "intent_status": "answerable",
            "generated_sql": "SELECT 2",
            "generated_sql_valid": True,
            "generated_execution_status": "passed",
            "ground_truth_execution_status": "passed",
            "expected_truncated": False,
            "actual_truncated": False,
            "result_match": False,
            "alias_only_difference": False,
            "type_only_difference": False,
            "order_only_mismatch": False,
            "error_category": "value_mismatch",
        },
    ]

    payload = summarize(records)

    assert payload["total"] == 2
    assert payload["result_value_match_rate"] == 0.5
    assert payload["alias_only_difference_count"] == 1
    assert payload["type_only_difference_count"] == 0
    assert payload["value_mismatch_count"] == 1
    json.dumps(payload)


def test_run_paths_create_per_run_result_folder(tmp_path):
    run_id = build_run_id("Extraction Run 001")
    paths = resolve_run_paths(
        tmp_path,
        results_root="evaluation/chatbot/results",
        run_id=run_id,
    )

    assert run_id == "Extraction_Run_001"
    assert paths.run_dir == tmp_path / "evaluation/chatbot/results/Extraction_Run_001"
    assert paths.output == paths.run_dir / "results.json"
    assert paths.analysis_output == paths.run_dir / "analysis.md"
    assert paths.trace_output == paths.run_dir / "trace.jsonl"
