import pytest
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.decomposition import PCA
from mlutil.transform import SigmaClipper, QuantileClipper, ColumnSelector


@pytest.mark.parametrize(
    'X, X_new, sigma, sigma_low, sigma_high',
    [
        (
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 302.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 4.],
                'b': [-2., 1., 3., 2., -5, np.nan],
            }),
            3., None, None,
        ),
        (
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 302.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 4.],
                'b': [-2., 1., 3., 2., -5, np.nan],
            }),
            1., 3., 3.,
        ),
        (
            np.array([
                [np.nan, -1., 2., 1., 1., 302.],
                [-2., 1., 3., 2., -201, np.nan],
            ]).T,
            np.array([
                [np.nan, -1., 2., 1., 1., 4.],
                [-2., 1., 3., 2., -5, np.nan],
            ]).T,
            3., None, None,
        ),
    ]
)
def test_SigmaClipper(X, X_new, sigma, sigma_low, sigma_high):
    t = SigmaClipper(sigma=sigma, low_sigma=sigma_low, high_sigma=sigma_high)
    X_new_ = t.fit_transform(X)
    if isinstance(X, np.ndarray):
        np.testing.assert_allclose(X_new_, X_new)
    elif isinstance(X, pd.DataFrame):
        np.testing.assert_allclose(X_new_.values, X_new.values)
    else:
        raise TypeError(type(X))


@pytest.mark.parametrize(
    'X, X_new, factor, q_low, q_high',
    [
        (
            pd.DataFrame({
                'a': [np.nan, -1., 2., 0, 1., 302.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            pd.DataFrame({
                'a': [np.nan, -1., 2., 0, 1., 4.],
                'b': [-2., 1., 3., 2., -8., np.nan],
            }),
            3., .25, .75,
        ),
        (
            np.array([
                [np.nan, -1., 2., 0, 1., 302.],
                [-2., 1., 3., 2., -201, np.nan],
            ]).T,
            np.array([
                [np.nan, -1., 2., 0, 1., 4.],
                [-2., 1., 3., 2., -8., np.nan],
            ]).T,
            3., .25, .75,
        ),
    ]
)
def test_QuantileClipper(X, X_new, factor, q_low, q_high):
    t = QuantileClipper(factor=factor, low_quantile=q_low, high_quantile=q_high)
    X_new_ = t.fit_transform(X)
    if isinstance(X, np.ndarray):
        np.testing.assert_allclose(X_new_, X_new)
    elif isinstance(X, pd.DataFrame):
        np.testing.assert_allclose(X_new_.values, X_new.values)
    else:
        raise TypeError(type(X))


@pytest.mark.parametrize(
    'columns, regex, like',
    [
        (['a_dd', 'c_dd', 'd_dd'], None, None),
        (None, r'\_dd$', None),
        (None, None, r'_dd'),
    ]
)
def test_ColumnSelector_bijective(columns, regex, like):
    df = pd.DataFrame({
        'a_dd': [1., 2., 3., np.nan],
        'b_ff': [1., 2., 3., np.nan],
        'c_dd': [1., 2., 3., np.nan],
        'd_dd': [1., 2., 3., np.nan],
    })
    expected = pd.DataFrame({
        'a_dd': [1., 2., 3., 0],
        'b_ff': [1., 2., 3., np.nan],
        'c_dd': [1., 2., 3., 0],
        'd_dd': [1., 2., 3., 0],
    })
    t = ColumnSelector(
        SimpleImputer(strategy='constant', fill_value=0),
        columns=columns,
        columns_like=like,
        columns_regex=regex,
    )
    actual = t.fit_transform(df)
    pd.testing.assert_frame_equal(expected, actual)
    assert t.new_columns_ == list(actual.columns)


@pytest.mark.parametrize(
    'infer_new_columns, new_columns_attr, new_columns_prefix, remainder, expected_columns',
    [
        ('same_attr', 'categories_', None, 'passthrough', ['b_ff', 'a_dd_1', 'a_dd_2', 'c_dd_1', 'c_dd_4']),
        ('num', None, None, 'passthrough', ['b_ff', 'a_dd_c_dd_0', 'a_dd_c_dd_1', 'a_dd_c_dd_2', 'a_dd_c_dd_3']),
        ('num', None, 'a_c_dd', 'passthrough', ['b_ff', 'a_c_dd_0', 'a_c_dd_1', 'a_c_dd_2', 'a_c_dd_3']),
        ('num', None, None, 'drop', ['a_dd_c_dd_0', 'a_dd_c_dd_1', 'a_dd_c_dd_2', 'a_dd_c_dd_3']),
    ]
)
def test_ColumnSelector_with_OneHotEncoder(
    infer_new_columns,
    new_columns_attr,
    new_columns_prefix,
    remainder,
    expected_columns,
):
    df = pd.DataFrame({
        'a_dd': [1, 2, 2, 2],
        'b_ff': [1., 2., 3., np.nan],
        'c_dd': [1, 1, 4, 4],
    })
    t = ColumnSelector(
        OneHotEncoder(sparse=False),
        columns=['a_dd', 'c_dd'],
        infer_new_columns=infer_new_columns,
        new_columns_attr=new_columns_attr,
        new_columns_prefix=new_columns_prefix,
        remainder=remainder,
    )
    actual = t.fit_transform(df)
    assert list(actual.columns) == expected_columns


@pytest.mark.parametrize(
    'infer_new_columns, new_columns_attr, new_columns_prefix, remainder, expected_columns',
    [
        ('attr', 'powers_', None, 'passthrough', ['b_ff', 'a_dd_c_dd_[0 0]', 'a_dd_c_dd_[1 0]', 'a_dd_c_dd_[0 1]', 'a_dd_c_dd_[1 1]']),
        ('attr', 'powers_', 'a_c_dd', 'passthrough', ['b_ff', 'a_c_dd_[0 0]', 'a_c_dd_[1 0]', 'a_c_dd_[0 1]', 'a_c_dd_[1 1]']),
        ('num', None, None, 'passthrough', ['b_ff', 'a_dd_c_dd_0', 'a_dd_c_dd_1', 'a_dd_c_dd_2', 'a_dd_c_dd_3']),
        ('num', None, 'a_c_dd', 'passthrough', ['b_ff', 'a_c_dd_0', 'a_c_dd_1', 'a_c_dd_2', 'a_c_dd_3']),
        ('num', None, None, 'drop', ['a_dd_c_dd_0', 'a_dd_c_dd_1', 'a_dd_c_dd_2', 'a_dd_c_dd_3']),
    ]
)
def test_ColumnSelector_with_PolynomialFeatures(
    infer_new_columns,
    new_columns_attr,
    new_columns_prefix,
    remainder,
    expected_columns,
):
    df = pd.DataFrame({
        'a_dd': [1, 2, 2, 2],
        'b_ff': [1., 2., 3., np.nan],
        'c_dd': [1, 1, 4, 4],
    })
    t = ColumnSelector(
        PolynomialFeatures(degree=2, interaction_only=True),
        columns=['a_dd', 'c_dd'],
        infer_new_columns=infer_new_columns,
        new_columns_attr=new_columns_attr,
        new_columns_prefix=new_columns_prefix,
        remainder=remainder,
    )
    actual = t.fit_transform(df)
    assert list(actual.columns) == expected_columns


@pytest.mark.parametrize(
    'infer_new_columns, new_columns_attr, new_columns_prefix, remainder, expected_columns',
    [
        ('num', None, None, 'passthrough', ['b_ff', 'a_dd_c_dd_0']),
        ('num', None, 'a_c_dd', 'passthrough', ['b_ff', 'a_c_dd_0']),
        ('num', None, None, 'drop', ['a_dd_c_dd_0']),
    ]
)
def test_ColumnSelector_with_PCA(
    infer_new_columns,
    new_columns_attr,
    new_columns_prefix,
    remainder,
    expected_columns,
):
    df = pd.DataFrame({
        'a_dd': [1, 2, 2, 2],
        'b_ff': [1., 2., 3., np.nan],
        'c_dd': [1, 1, 4, 4],
    })
    t = ColumnSelector(
        PCA(n_components=1),
        columns=['a_dd', 'c_dd'],
        infer_new_columns=infer_new_columns,
        new_columns_attr=new_columns_attr,
        new_columns_prefix=new_columns_prefix,
        remainder=remainder,
    )
    actual = t.fit_transform(df)
    assert list(actual.columns) == expected_columns


@pytest.mark.parametrize(
    'X, X_new, columns',
    [
        (
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 302.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 4.],
                'b': [-2., 1., 3., 2., -5, np.nan],
            }),
            None,
        ),
        (
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 302.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            pd.DataFrame({
                'a': [np.nan, -1., 2., 1., 1., 4.],
                'b': [-2., 1., 3., 2., -201, np.nan],
            }),
            ['a'],
        ),
    ]
)
def test_ColumnSelector_with_SigmaClipper(X, X_new, columns):
    t = ColumnSelector(
        SigmaClipper(low_sigma=3, high_sigma=3),
        columns=columns,
    )
    X_new_ = t.fit_transform(X)
    if isinstance(X, np.ndarray):
        np.testing.assert_allclose(X_new_, X_new)
    elif isinstance(X, pd.DataFrame):
        np.testing.assert_allclose(X_new_.values, X_new.values)
    else:
        raise TypeError(type(X))
