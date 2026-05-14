from health_system_chatbot.artifacts import load_stage1_context


def test_load_stage1_context_reads_v2_benchmark_and_join_policy():
    ctx = load_stage1_context()

    assert len(ctx.ground_truth) == 100
    assert "internacoes" in ctx.tables
    assert any(policy.confidence == "rejected" for policy in ctx.join_policies)
    assert any(
        policy.accepted_usage_policy == "left_join_or_explicit_mapped_scope_required"
        for policy in ctx.join_policies
    )

