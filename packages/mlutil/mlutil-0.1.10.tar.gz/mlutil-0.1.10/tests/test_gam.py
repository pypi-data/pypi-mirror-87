import numpy as np
from mlutil.model import GAM


def test_GAM():
    m = GAM()
    X = np.arange(20)[:, None]
    y = np.arange(20) + np.random.normal(scale=0.1, size=20)
    m.fit(X, y)
    X_test = np.arange(15, 25)[:, None]
    y_test = np.arange(15, 25)
    y_hat = m.predict(X_test)
    np.testing.assert_allclose(y_test, y_hat, atol=1.)
