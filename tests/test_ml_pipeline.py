"""Tests for QML pipeline."""

from __future__ import annotations

from quonic.ml import QMLPipeline


def test_pipeline_creation():
    """Pipeline should be created with correct parameters."""
    pipe = QMLPipeline(n_qubits=2, layers=2)
    assert pipe.n_qubits == 2
    assert pipe.layers == 2
    assert pipe.params is None


def test_pipeline_repr():
    """Pipeline should have readable repr."""
    pipe = QMLPipeline(n_qubits=2)
    r = repr(pipe)
    assert "QMLPipeline" in r
    assert "trained=False" in r


def test_pipeline_predict_before_fit():
    """Predict before fit should raise."""
    pipe = QMLPipeline(n_qubits=2)
    try:
        pipe.predict([[0.0, 0.0]])
        assert False, "Should have raised"
    except RuntimeError:
        pass


def test_pipeline_fit_and_predict():
    """Pipeline should fit and predict."""
    pipe = QMLPipeline(n_qubits=2, layers=1, optimizer="spsa", lr=0.1)
    X = [[0.0, 0.0], [0.5, 0.5], [1.0, 0.0]]
    y = [0.0, 0.5, 1.0]
    result = pipe.fit(X, y, maxiter=10)
    assert result.train_result.n_steps == 10
    assert result.predictions is not None
    assert len(result.predictions) == 3
