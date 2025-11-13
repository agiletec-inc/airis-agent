from airis_agent.api.deep_research import ResearchRequest, perform_research


def test_perform_research_with_seed_sources():
    request = ResearchRequest(
        query="Supabase auth best practices",
        depth="quick",
        seed_sources=["https://supabase.com/docs", "https://github.com/supabase"],
    )

    response = perform_research(request)

    assert response.plan  # waves present
    assert response.sources
    assert response.confidence >= 0.85
    assert "Supabase" in response.summary
