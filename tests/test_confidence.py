from backend.main import compute_confidence


class ProbabilityPipeline:
    def predict_proba(self, texts):
        return [[0.2, 0.8]]


class DecisionPipeline:
    def decision_function(self, texts):
        return [[0.0, 2.0]]


def test_uses_highest_predicted_probability():
    assert compute_confidence(ProbabilityPipeline(), "text") == 0.8


def test_converts_decision_scores_to_probability():
    confidence = compute_confidence(DecisionPipeline(), "text")
    assert 0.8 < confidence < 1.0


def test_falls_back_when_model_has_no_confidence_method():
    assert compute_confidence(object(), "text") == 1.0
