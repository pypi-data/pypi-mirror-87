import numpy as np
import pandas as pd
import statsmodels.api as sm
import sklearn.covariance as skcov
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from numpy.linalg import inv


def mean_vector(X, method="hist", d=0.94):
    r"""
    Calculate the expected returns vector using the selected method.

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.   
    method : str, can be {'hist', 'ewma1' or 'ewma2'}
        The method used to estimate the expected returns. 
        The default value is 'hist'.
        
        - 'hist': use historical estimates.
        - 'ewma1'': use ewma with adjust=True, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
        - 'ewma2': use ewma with adjust=False, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
    d : scalar
        The smoothing factor of ewma methods.
        The default is 0.94.
    
    Returns
    -------
    mu : 1d-array
        The estimation of expected returns.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.

    """

    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    assets = X.columns.tolist()

    if method == "hist":
        mu = np.array(X.mean(), ndmin=2)
    elif method == "ewma1":
        mu = np.array(X.ewm(alpha=1 - d).mean().iloc[-1, :], ndmin=2)
    elif method == "ewma2":
        mu = np.array(X.ewm(alpha=1 - d, adjust=False).mean().iloc[-1, :], ndmin=2)

    mu = pd.DataFrame(np.array(mu, ndmin=2), columns=assets)

    return mu


def covar_matrix(X, method="hist", d=0.94, **kwargs):
    r"""
    Calculate the covariance matrix using the selected method.
    
    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.    
    method : str, can be {'hist', 'ewma1', 'ewma2', 'ledoit', 'oas' or 'shrunk'}
        The default is 'hist'. The method used to estimate the covariance matrix:
        
        - 'hist': use historical estimates.
        - 'ewma1'': use ewma with adjust=True, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
        - 'ewma2': use ewma with adjust=False, see `EWM <https://pandas.pydata.org/pandas-docs/stable/user_guide/computation.html#exponentially-weighted-windows>`_ for more details.
        - 'ledoit': use the Ledoit and Wolf Shrinkage method.
        - 'oas': use the Oracle Approximation Shrinkage method.
        - 'shrunk': use the basic Shrunk Covariance method.
    d : scalar
        The smoothing factor of ewma methods.
        The default is 0.94.            
    **kwargs:
        Other variables related to covariance estimation. See
        `Scikit Learn <https://scikit-learn.org/stable/modules/covariance.html>`_
        for more details.
    
    Returns
    -------
    cov : nd-array
        The estimation of covariance matrix.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.
        
    """

    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    assets = X.columns.tolist()

    if method == "hist":
        cov = np.cov(X.T)
    elif method == "ewma1":
        cov = X.ewm(alpha=1 - d).cov()
        item = cov.iloc[-1, :].name[0]
        cov = cov.loc[(item, slice(None)), :]
    elif method == "ewma2":
        cov = X.ewm(alpha=1 - d, adjust=False).cov()
        item = cov.iloc[-1, :].name[0]
        cov = cov.loc[(item, slice(None)), :]
    elif method == "ledoit":
        lw = skcov.LedoitWolf(**kwargs)
        lw.fit(X)
        cov = lw.covariance_
    elif method == "oas":
        oas = skcov.OAS(**kwargs)
        oas.fit(X)
        cov = oas.covariance_
    elif method == "shrunk":
        sc = skcov.ShrunkCovariance(**kwargs)
        sc.fit(X)
        cov = sc.covariance_

    cov = pd.DataFrame(np.array(cov, ndmin=2), columns=assets, index=assets)

    return cov


def forward_regression(X, y, criterion="pvalue", threshold=0.05, verbose=False):
    r"""
    Select the variables that estimate the best model using stepwise
    forward regression.

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    y : Series of shape (n_samples, 1)
        Target vector, where n_samples in the number of samples.
    criterion : str, can be {'pvalue', 'AIC', 'SIC', 'R2' or 'R2_A'}
        The default is 'pvalue'. The criterion used to select the best features:
        
        - 'pvalue': select the features based on p-values.
        - 'AIC': select the features based on lowest Akaike Information Criterion.
        - 'SIC': select the features based on lowest Schwarz Information Criterion.
        - 'R2': select the features based on highest R Squared.
        - 'R2_A': select the features based on highest Adjusted R Squared.
    thresholdt : scalar, optional
        Is the maximum p-value for each variable that will be 
        accepted in the model. The default is 0.05.
    verbose : bool, optional
        Enable verbose output. The default is False.

    Returns
    -------
    value : list    
        A list of the variables that produce the best model.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.

    """
    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    if not isinstance(y, pd.DataFrame) and not isinstance(y, pd.Series):
        raise ValueError("y must be a column DataFrame")

    if isinstance(y, pd.DataFrame):
        if y.shape[0] > 1 and y.shape[1] > 1:
            raise ValueError("y must be a column DataFrame")

    included = []
    aic = 1e10
    sic = 1e10
    r2 = -1e10
    r2_a = -1e10

    if criterion == "pvalue":
        value = 0
        while value <= threshold:
            excluded = list(set(X.columns) - set(included))
            best_pvalue = 999999
            new_feature = None
            for i in excluded:
                factors = included + [i]
                X1 = X[factors]
                X1 = sm.add_constant(X1)
                results = sm.OLS(y, X1).fit()
                new_pvalues = results.pvalues
                cond_1 = new_pvalues[new_pvalues.index != "const"].max()
                if best_pvalue > new_pvalues[i] and cond_1 <= threshold:
                    best_pvalue = results.pvalues[i]
                    new_feature = i
                    pvalues = new_pvalues.copy()

            value = pvalues[pvalues.index != "const"].max()

            if new_feature is None:
                break

            included.append(new_feature)

            if verbose:
                print("Add {} with p-value {:.6}".format(new_feature, best_pvalue))

    else:
        excluded = X.columns.tolist()
        for i in range(X.shape[1]):
            j = 0
            value = None
            for i in excluded:
                factors = included.copy()
                factors.append(i)
                X1 = X[factors]
                X1 = sm.add_constant(X1)
                results = sm.OLS(y, X1).fit()

                if criterion == "AIC":
                    if results.aic < aic:
                        value = i
                        aic = results.aic
                if criterion == "SIC":
                    if results.bic < sic:
                        value = i
                        sic = results.bic
                if criterion == "R2":
                    if results.rsquared > r2:
                        value = i
                        r2 = results.rsquared
                if criterion == "R2_A":
                    if results.rsquared_adj > r2_a:
                        value = i
                        r2_a = results.rsquared_adj

                j += 1
                if j == len(excluded):
                    if value is None:
                        break
                    else:
                        excluded.remove(value)
                        included.append(value)
                        if verbose:
                            if criterion == "AIC":
                                print(
                                    "Add {} with AIC {:.6}".format(value, results.aic)
                                )
                            elif criterion == "SIC":
                                print(
                                    "Add {} with SIC {:.6}".format(value, results.bic)
                                )
                            elif criterion == "R2":
                                print(
                                    "Add {} with R2 {:.6}".format(
                                        value, results.rsquared
                                    )
                                )
                            elif criterion == "R2_A":
                                print(
                                    "Add {} with Adjusted R2 {:.6}".format(
                                        value, results.rsquared_adj
                                    )
                                )

    return included


def backward_regression(X, y, criterion="pvalue", threshold=0.05, verbose=False):
    r"""
    Select the variables that estimate the best model using stepwise 
    backward regression.        

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    y : Series of shape (n_samples, 1)
        Target vector, where n_samples in the number of samples.
    criterion : str, can be {'pvalue', 'AIC', 'SIC', 'R2' or 'R2_A'}
        The default is 'pvalue'. The criterion used to select the best features:
        
        - 'pvalue': select the features based on p-values.
        - 'AIC': select the features based on lowest Akaike Information Criterion.
        - 'SIC': select the features based on lowest Schwarz Information Criterion.
        - 'R2': select the features based on highest R Squared.
        - 'R2_A': select the features based on highest Adjusted R Squared.
    threshold : scalar, optional
        Is the maximum p-value for each variable that will be 
        accepted in the model. The default is 0.05.
    verbose : bool, optional
        Enable verbose output. The default is False.

    Returns
    -------
    value : list    
        A list of the variables that produce the best model.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.
        
    """

    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    if not isinstance(y, pd.DataFrame) and not isinstance(y, pd.Series):
        raise ValueError("y must be a column DataFrame")

    if isinstance(y, pd.DataFrame):
        if y.shape[0] > 1 and y.shape[1] > 1:
            raise ValueError("y must be a column DataFrame")

    X1 = sm.add_constant(X)
    results = sm.OLS(y, X1).fit()
    pvalues = results.pvalues
    aic = results.aic
    sic = results.bic
    r2 = results.rsquared
    r2_a = results.rsquared_adj

    included = pvalues.index.tolist()
    excluded = ["const"]

    if criterion == "pvalue":
        while pvalues[pvalues.index != "const"].max() > threshold:
            factors = pvalues[~pvalues.index.isin(excluded)].index.tolist()
            X1 = X[factors]
            X1 = sm.add_constant(X1)
            results = sm.OLS(y, X1).fit()
            pvalues = results.pvalues
            pvalues = pvalues[pvalues.index != "const"]
            excluded = ["const", pvalues.idxmax()]
            if verbose and pvalues.max() > threshold:
                print(
                    "Drop {} with p-value {:.6}".format(pvalues.idxmax(), pvalues.max())
                )

        included = pvalues.index.tolist()

    else:
        included.remove("const")
        for i in range(X.shape[1]):
            j = 0
            value = None
            for i in included:
                factors = included.copy()
                factors.remove(i)
                X1 = X[factors]
                X1 = sm.add_constant(X1)
                results = sm.OLS(y, X1).fit()

                if criterion == "AIC":
                    if results.aic < aic:
                        value = i
                        aic = results.aic
                elif criterion == "SIC":
                    if results.bic < sic:
                        value = i
                        sic = results.bic
                elif criterion == "R2":
                    if results.rsquared > r2:
                        value = i
                        r2 = results.rsquared
                elif criterion == "R2_A":
                    if results.rsquared_adj > r2_a:
                        value = i
                        r2_a = results.rsquared_adj

                j += 1
                if j == len(included):
                    if value is None:
                        break
                    else:
                        included.remove(value)
                        if verbose:
                            if criterion == "AIC":
                                print(
                                    "Drop {} with AIC {:.6}".format(value, results.aic)
                                )
                            elif criterion == "SIC":
                                print(
                                    "Drop {} with SIC {:.6}".format(value, results.bic)
                                )
                            elif criterion == "R2":
                                print(
                                    "Drop {} with R2 {:.6}".format(
                                        value, results.rsquared
                                    )
                                )
                            elif criterion == "R2_A":
                                print(
                                    "Drop {} with Adjusted R2 {:.6}".format(
                                        value, results.rsquared_adj
                                    )
                                )

    return included


def PCR(X, y, n_components=0.95):
    r"""
    Estimate the coeficients using Principal Components Regression (PCR).        

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    y : Series of shape (n_samples, 1)
        Target vector, where n_samples in the number of samples.
    n_components : int, float, None or str, optional
        if 1 < n_components (int), it represents the number of components that
        will be keep. if 0 < n_components < 1 (float), it represents the
        percentage of variance that the is explained by the components keeped. 
        See `PCA <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>`_
        for more details. The default is 0.95.

    Returns
    -------
    value : nd-array    
        An array with the coefficients of the model calculated using PCR.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.
        
    """

    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    if not isinstance(y, pd.DataFrame) and not isinstance(y, pd.Series):
        raise ValueError("y must be a column DataFrame")

    if isinstance(y, pd.DataFrame):
        if y.shape[0] > 1 and y.shape[1] > 1:
            raise ValueError("y must be a column DataFrame")

    scaler = StandardScaler()
    scaler.fit(X)
    X_std = scaler.transform(X)

    pca = PCA(n_components=n_components)
    pca.fit(X_std)
    Z_p = pca.transform(X_std)
    V_p = pca.components_.T

    results = sm.OLS(y, sm.add_constant(Z_p)).fit()
    beta_pc = results.params[1:]
    beta_pc = np.array(beta_pc, ndmin=2)

    std = np.array(np.std(X, axis=0, ddof=1), ndmin=2)
    mean = np.array(np.mean(X, axis=0), ndmin=2)
    beta = V_p @ beta_pc.T / std.T

    beta_0 = np.array(y.mean(), ndmin=2) - np.sum(beta * mean.T)

    beta = np.insert(beta, 0, beta_0)
    beta = np.array(beta, ndmin=2)

    return beta


def loadings_matrix(
    X,
    Y,
    feature_selection="stepwise",
    stepwise="Forward",
    criterion="pvalue",
    threshold=0.05,
    n_components=0.95,
    verbose=False,
):
    r"""
    Estimate the loadings matrix using stepwise regression.        

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    Y : DataFrame of shape (n_samples, n_assets)
        Target matrix, where n_samples in the number of samples and 
        n_assets is the number of assets.
    feature_selection: str 'stepwise' or 'PCR', optional
        Indicate the method used to estimate the loadings matrix.
        The default is 'stepwise'.
    stepwise: str 'Forward' or 'Backward', optional
        Indicate the method used for stepwise regression.
        The default is 'Forward'.
    criterion : str, can be {'pvalue', 'AIC', 'SIC', 'R2' or 'R2_A'}
        The default is 'pvalue'. The criterion used to select the best features:
        
        - 'pvalue': select the features based on p-values.
        - 'AIC': select the features based on lowest Akaike Information Criterion.
        - 'SIC': select the features based on lowest Schwarz Information Criterion.
        - 'R2': select the features based on highest R Squared.
        - 'R2_A': select the features based on highest Adjusted R Squared.
    threshold : scalar, optional
        Is the maximum p-value for each variable that will be 
        accepted in the model. The default is 0.05.
    n_components : int, float, None or str, optional
        if 1 < n_components (int), it represents the number of components that
        will be keep. if 0 < n_components < 1 (float), it represents the
        percentage of variance that the is explained by the components keeped. 
        See `PCA <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>`_
        for more details. The default is 0.95.
    verbose : bool, optional
        Enable verbose output. The default is False.
        
    Returns
    -------
    loadings : DataFrame    
        A DataFrame with the loadings matrix.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.
        
    """
    if not isinstance(X, pd.DataFrame):
        raise ValueError("X must be a DataFrame")

    if not isinstance(Y, pd.DataFrame):
        raise ValueError("Y must be a DataFrame")

    rows = Y.columns.tolist()
    cols = X.columns.tolist()
    cols.insert(0, "const")
    loadings = np.zeros((len(rows), len(cols)))
    loadings = pd.DataFrame(loadings, index=rows, columns=cols)

    for i in rows:
        if feature_selection == "stepwise":
            if stepwise == "Forward":
                included = forward_regression(
                    X, Y[i], criterion=criterion, threshold=threshold, verbose=verbose
                )
            elif stepwise == "Backward":
                included = backward_regression(
                    X, Y[i], criterion=criterion, threshold=threshold, verbose=verbose
                )
            else:
                raise ValueError("Choose and adecuate stepwise method")
            results = sm.OLS(Y[i], sm.add_constant(X[included])).fit()
            params = results.params
            loadings.loc[i, params.index.tolist()] = params.T
        elif feature_selection == "PCR":
            beta = PCR(X, Y[i], n_components=n_components)
            beta = pd.Series(np.ravel(beta), index=cols)
            loadings.loc[i, cols] = beta.T

    return loadings


def risk_factors(
    X,
    Y,
    B=None,
    method_mu="hist",
    method_cov="hist",
    feature_selection="stepwise",
    stepwise="Forward",
    criterion="pvalue",
    threshold=0.05,
    n_components=0.95,
    error=True,
    **kwargs
):
    r"""
    Estimate the expected returns vector and covariance matrix based on risk
    factors models :cite:`b-Ross` :cite:`b-Fan`.

    .. math::
        R = \alpha + B F + \epsilon 

    .. math::
        \mu_{f} = \alpha +BE(F)

    .. math::
        \Sigma_{f} = B \Sigma_{F} B^{T} + \Sigma_{\epsilon}

    where:
    
    :math:`R` is the series returns.
        
    :math:`\alpha` is the intercept.

    :math:`B` is the loadings matrix.
    
    :math:`F` is the expected returns vector of the risk factors.

    :math:`\Sigma_{F}` is the covariance matrix of the risk factors.

    :math:`\Sigma_{\epsilon}` is the covariance matrix of error terms.

    :math:`\mu_{f}` is the expected returns vector obtained with the
    risk factor model.
    
    :math:`\Sigma_{f}` is the covariance matrix obtained with the risk
    factor model.
        
    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Features matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    Y : DataFrame of shape (n_samples, n_assets)
        Target matrix, where n_samples in the number of samples and 
        n_assets is the number of assets.
    B : DataFrame of shape (n_assets, n_features), optional
        Loadings matrix. If is not specified, is estimated using
        stepwise regression. The default is None.
    method: str 'stepwise' or 'PCR', optional
        Indicate the method used to estimate the loadings matrix.
        The default is 'stepwise'.
    stepwise: str 'Forward' or 'Backward'
        Indicate the method used for stepwise regression. 
        The default is 'Forward'.
    criterion : str, can be {'pvalue', 'AIC', 'SIC', 'R2' or 'R2_A'}
        The default is 'pvalue'. The criterion used to select the best features:
        
        - 'pvalue': select the features based on p-values.
        - 'AIC': select the features based on lowest Akaike Information Criterion.
        - 'SIC': select the features based on lowest Schwarz Information Criterion.
        - 'R2': select the features based on highest R Squared.
        - 'R2_A': select the features based on highest Adjusted R Squared.
    threshold : scalar, optional
        Is the maximum p-value for each variable that will be 
        accepted in the model. The default is 0.05.
    n_components : int, float, None or str, optional
        if 1 < n_components (int), it represents the number of components that
        will be keep. if 0 < n_components < 1 (float), it represents the
        percentage of variance that the is explained by the components keeped. 
        See `PCA <https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html>`_
        for more details. The default is 0.95.
    error : bool
        Indicate if diagonal covariance matrix of errors is included (only 
        when B is estimated through a regression).
    **kwargs : dict
        Other variables related to the expected returns and covariance estimation.

    Returns
    -------
    mu : DataFrame    
        The mean vector of risk factors model.
    cov : DataFrame
        The covariance matrix of risk factors model.
    returns : DataFrame
        The returns based on a risk factor model.
    nav : DataFrame
        The cumulated uncompound returns based on a risk factor model.        

    Raises
    ------
    ValueError
        When the value cannot be calculated.
               
    """
    if not isinstance(X, pd.DataFrame) and not isinstance(Y, pd.DataFrame):
        raise ValueError("X and Y must be DataFrames")

    if B is None:
        B = loadings_matrix(
            X,
            Y,
            feature_selection=feature_selection,
            stepwise=stepwise,
            criterion=criterion,
            threshold=threshold,
            n_components=n_components,
            verbose=False,
        )
        X1 = sm.add_constant(X)
    elif not isinstance(B, pd.DataFrame):
        raise ValueError("B must be a DataFrame")
    elif isinstance(B, pd.DataFrame):
        X1 = X.copy()

    assets = Y.columns.tolist()
    dates = X.index.tolist()

    mu_f = np.array(mean_vector(X1, method=method_mu, **kwargs), ndmin=2)
    S_f = np.array(covar_matrix(X1, method=method_cov, **kwargs), ndmin=2)
    B = np.array(B, ndmin=2)

    returns = np.array(X1, ndmin=2) @ B.T
    mu = B @ mu_f.T

    if error == True:
        e = np.array(Y, ndmin=2) - returns
        S_e = np.diag(np.var(np.array(e), ddof=1, axis=0))
        S = B @ S_f @ B.T + S_e
    elif error == False:
        S = B @ S_f @ B.T

    mu = pd.DataFrame(mu.T, columns=assets)
    cov = pd.DataFrame(S, index=assets, columns=assets)
    returns = pd.DataFrame(returns, index=dates, columns=assets)
    nav = returns.cumsum()

    return mu, cov, returns, nav


def black_litterman(
    X, w, P, Q, delta=1, rf=0, eq=True, method_mu="hist", method_cov="hist", **kwargs
):
    r"""
    Estimate the expected returns vector and covariance matrix based 
    on the black litterman model :cite:`b-BlackLitterman` :cite:`b-Black1`.
    
    .. math::
        \Pi = \delta \Sigma w

    .. math::
        \Pi_{bl} = \left[(\tau\Sigma)^{-1}+ P \Omega^{-1}P \right]^{-1}
        \left[(\tau\Sigma)^{-1} \Pi + P \Omega^{-1}Q \right]

    .. math::        
        M = \left((\tau\Sigma)^{-1} + P'\Omega^{-1} P \right)^{-1}

    .. math::        
        \mu_{bl} = \Pi_{bl} + rf

    .. math::
        \Sigma_{bl} = \Sigma + M
        
    where:

    :math:`rf` is the risk free rate.

    :math:`\delta` is the risk aversion factor.

    :math:`\Pi` is the equilibrium excess returns.
    
    :math:`\Sigma` is the covariance matrix.

    :math:`P` is the views matrix.

    :math:`Q` is the views returns matrix.

    :math:`\Omega` is covariance matrix of the error views.

    :math:`\mu_{bl}` is the mean vector obtained with the black
    litterman model.
    
    :math:`\Sigma_{bl}` is the covariance matrix obtained with the black
    litterman model.

    Parameters
    ----------
    X : DataFrame of shape (n_samples, n_features)
        Assets matrix, where n_samples is the number of samples and 
        n_features is the number of features.
    w : DataFrame of shape (n_assets, 1)
        Weights matrix, where n_assets is the number of assets.
    P : DataFrame of shape (n_views, n_assets)
        Analyst's views matrix, can be relative or absolute.    
    Q : DataFrame of shape (n_views, 1)
        Expected returns of analyst's views.
    delta : float, optional
        Risk aversion factor. The default value is 1.        
    rf : scalar, optional
        Risk free rate. The default is 0.
    eq : bool, optional
        Indicate if use equilibrum or historical excess returns. 
        The default is True.
    **kwargs : dict
        Other variables related to the expected returns and covariance estimation.
        
    Returns
    -------
    mu : DataFrame    
        The mean vector of black litterman model.
    cov : DataFrame
        The covariance matrix of black litterman model.
        
    Raises
    ------
    ValueError
        When the value cannot be calculated.

    """
    if not isinstance(X, pd.DataFrame) and not isinstance(w, pd.DataFrame):
        raise ValueError("X and w must be DataFrames")

    if w.shape[0] > 1 and w.shape[1] > 1:
        raise ValueError("w must be a column DataFrame")

    assets = X.columns.tolist()

    w = np.array(w, ndmin=2)
    if w.shape[0] == 1:
        w = w.T

    mu = np.array(mean_vector(X, method=method_mu, **kwargs), ndmin=2)
    S = np.array(covar_matrix(X, method=method_cov, **kwargs), ndmin=2)
    P = np.array(P, ndmin=2)
    Q = np.array(Q, ndmin=2)
    tau = 1 / X.shape[0]
    Omega = np.array(np.diag(np.diag(P @ (tau * S) @ P.T)), ndmin=2)

    if eq == True:
        PI = delta * (S @ w)
    elif eq == False:
        PI = mu.T - rf

    PI_ = inv(inv(tau * S) + P.T @ inv(Omega) @ P) @ (
        inv(tau * S) @ PI + P.T @ inv(Omega) @ Q
    )
    M = inv(inv(tau * S) + P.T @ inv(Omega) @ P)
    # PI_1 = PI + (tau * S* P.T) * inv(P * tau * S * P.T + Omega) * (Q - P * PI)
    # M = tau * S - (tau * S * P.T) * inv(P * tau * S * P.T + Omega) * P * tau * S

    mu = PI_ + rf
    mu = mu.T
    cov = S + M
    w = (1 / (1 + tau)) * inv(delta * cov) @ PI_

    mu = pd.DataFrame(mu, columns=assets)
    cov = pd.DataFrame(cov, index=assets, columns=assets)
    w = pd.DataFrame(w, index=assets)

    return mu, cov, w
