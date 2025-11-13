from airis_agent.api.confidence import (
    ConfidenceRequest,
    ConfidenceResponse,
    evaluate_confidence,
)


def test_confidence_high_action():
    request = ConfidenceRequest(
        task="Ship feature",
        duplicate_check_complete=True,
        architecture_check_complete=True,
        official_docs_verified=True,
        oss_reference_complete=True,
        root_cause_identified=True,
    )

    response = evaluate_confidence(request)
    assert isinstance(response, ConfidenceResponse)
    assert response.score >= 0.9
    assert response.action == "proceed"
    assert response.checks


def test_confidence_low_action():
    request = ConfidenceRequest(
        task="Investigate bug",
        duplicate_check_complete=False,
        architecture_check_complete=False,
        official_docs_verified=False,
        oss_reference_complete=False,
        root_cause_identified=False,
    )

    response = evaluate_confidence(request)
    assert response.score <= 0.5
    assert response.action == "stop"
