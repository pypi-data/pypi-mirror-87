"""
t_test.py
~~~~~~~~~
This module provides functionality for conducting t-tests. It includes the ability to conduct
1) one-sample t-test, 2) paired-samples/repeated-measures/within-subjects t-test, and 3)
independent-samples/between-subjects t-test.
"""

# Related third-party library.
from scipy.stats import norm, t

def t_test(x, y=None, alternative="two-tailed", mu=None, data=None, paired=False, conf_level=0.05,
           subset=None):
    """
    Conducts a t-test.

    :param x:           The column of the first sample. If ``data`` is not ``None``, then a string
                        providing the column title may be provided.
    :type x:            ``EzPyZ.column.Column`` or ``str``
    :param y:           (optional) The column of the second sample. If ``data`` is not ``None``,
                        then a string providing the column title may be provided. If
                        performing a one-sample t-test, this should not be used. Defaults to
                        ``None``.
    :type y:            ``EzPyZ.column.Column`` or ``str``
    :param alternative: (optional) String. Whether the x column is being tested to be greater than,
                        less than, or not equal to the y column. Must be one of "two-tailed",
                        "less", or "greater". Defaults to "two-tailed".
    :type alternative:  ``str``
    :param mu:          (optional) Float. The population mean for a one-sample t-test. Defaults to
                        ``None``.
    :type mu:           ``float``
    :param data:        (optional) The dataframe containing the values. Defaults to ``None``
    :type data:         ``EzPyZ.DataFrame``
    :param paired:      (optional) Boolean. Whether the t-test is a paired-samples t-test. If
                        ``False``, an independent-samples t-test is conducted. Defaults to
                        ``False``.
    :type paired:       ``bool``
    :param conf_level:  (optional) Float. The confidence interval. Defaults to ``0.05``.
    :type conf_level:   ``float``
    :param subset:      (optional) String containing rules to exclude cetain rows from the analysis.
                        See ``EzPyZ.DataFrame`` for more information on writing these strings.
                        **This parameter may only be used when** ``data`` **is set to a valid**
                        ``EzPyZ.DataFrame``! Defaults to ``None``.
    :type subset:       ``str``
    :return:            The results of the t-test.
    :rtype:             ``EzPyZ.TResult``

    Example one-sample t-test::

        >>> import EzPyZ as ez
        >>> data = {
        ...     'score': [15, 17, 16, 16, 19, 14, 17]
        ... }
        >>> df = ez.DataFrame(data)
        >>> # Let's conduct a two-tailed, one-sample t-test between the scores and a population mean,
        >>> # in this case well say 12.
        >>> # We'll also use the standard confidence level of 0.05.
        >>> t_res = ez.t_test(data=df, x='score', mu=15)
        >>> print(t_res)

                                One-sample t-test

        data:   score
        t = 7.0711, df = 6, p-value = 0.000401
        null hypothesis:                        true difference in means is equal to 0
        alternative hypothesis:                 true difference in means is not equal to 0
        resolution:                             reject null hypothesis with confidence level of 0.05
        95.0 percent confidence interval for x: [13.14278, 19.428649]
        mean of the differences (μ - x):        -4.285714

    Example independent-samples t-test::

        >>> import EzPyZ as ez
        >>> data = {
        ...     'before': [1, 3, 4, 2, 3, 4, 6],
        ...     'after': [3, 4, 6, 9, 8, 7, 11]
        ... }
        >>> df = ez.DataFrame(data)
        >>> # Let's conduct a two-tailed, independent-samples t-test between the before and after
        >>> # scores.
        >>> # We'll also use the standard confidence level of 0.05.
        >>> t_res = ez.t_test(data=df, x='before', y='after', paired=True)
        >>> print(t_res)

                                Welch Two-Sample t-test

        data:   before and after
        t = -2.9327, df = 9.5647, p-value = 0.015663
        null hypothesis:                        true difference in means is equal to 0
        alternative hypothesis:                 true difference in means is not equal to 0
        resolution:                             reject null hypothesis with confidence level of 0.05
        95.0 percent confidence interval for x: [0.14278, 6.428649]
        mean of the differences (y - x):        3.571429

    Example paired-samples t-test::

        >>> import EzPyZ as ez
        >>> data = {
        ...     'before': [1, 3, 4, 2, 3, 4, 6],
        ...     'after': [3, 4, 6, 9, 8, 7, 11]
        ... }
        >>> df = ez.DataFrame(data)
        >>> # Let's conduct a two-tailed, paired-samples t-test between the before and after scores.
        >>> # We'll also use the standard confidence level of 0.05.
        >>> t_res = ez.t_test(data=df, x='before', y='after', paired=True)
        >>> print(t_res)

                                                Paired t-test

        data:                                                   before (m = 3.29) and after (m = 6.86)
        output:                                                 t = -4.3966, df = 6, p-value = 0.004585
        null hypothesis:                                        true difference in means is equal to 0
        alternative hypothesis:                                 true difference in means is not equal to 0
        resolution:                                             reject null hypothesis with confidence level of 0.05
        95.0 percent confidence interval for x:                 [0.14278, 6.428649]
        mean of the differences (y - x):                        3.571429

    """
    # Validate input.
    if alternative not in ["two-tailed", "less", "greater"]:
        raise ValueError(alternative + " is not a valid option for ``alternative``!")
    if y is None and mu is None:
        raise ValueError("either ``y`` or ``mu`` must be specified!")
    if subset is not None and data is None:
        raise Warning("data parameter is not set! subset parameter will be ignored!")

    # Filter data if applicable.
    if subset is not None and data is not None:
        data = data.subset(subset)

    if data is not None:
        x = getattr(data, x)
        if mu is None:
            y = getattr(data, y)

    # Conduct t-test.
    results = {
        'description': None,
        'options': {
            'x': x,
            'y': None,
            'mu': None,
            'confidence_level': conf_level,
            'alternative': alternative
        },
        'output': None
    }

    if mu is not None:
        # Conduct a one-sample t-test.
        results['description'] = "One-sample t-test"
        results['options']['mu'] = mu
        df = x.length() - 1
        t_score = (x.mean() - mu)/(x.stdev()/x.length()**(1/2))
    elif not paired:
        # Conduct an independent-samples t-test.
        # A Welch's t-test will be conducted (it is more robust with respect to
        # homoschedasticity).
        results['description'] = "Welch Two-Sample t-test"
        results['options']['y'] = y

        t_score = ((x.mean() - y.mean())/((x.variance()/x.length())
                    + (y.variance()/y.length()))**(1/2))
        dft = ((x.variance()/x.length()) + (y.variance()/y.length()))**2
        dfb = ((x.variance()**2)/(x.length()**2 * (x.length() - 1))
                + (y.variance()**2)/(y.length()**2 * (y.length() - 1)))
        df = dft/dfb
    else:
        # Conduct a paired-samples t-test.
        results['description'] = "Paired t-test"
        results['options']['y'] = y

        x_vals = x.get_values()
        y_vals = y.get_values()
        df = len(x_vals) - 1
        s_dev = 0
        devs = []
        for i in range(len(x_vals)):
            dev = x_vals[i] - y_vals[i]
            s_dev += dev
            devs.append(dev)
        m_dev = s_dev / len(x_vals)
        ss_dev_dev = 0
        for dev in devs:
            ss_dev_dev += (dev - m_dev)**2
        d_var = ss_dev_dev/df
        stdev_m = (d_var/len(x_vals))**(1/2)

        t_score = m_dev/stdev_m

    p = t.sf(abs(t_score), df)
    if alternative == "two-tailed":
        p *= 2
        conf_z_score = abs(norm.ppf(conf_level/2))
        conf_interval = [
            x.mean() - (x.stdev() * conf_z_score),
            x.mean() + (x.stdev() * conf_z_score)
        ]
    elif alternative == "greater":
        conf_z_score = abs(norm.ppf(conf_level))
        conf_interval = [
            x.mean() - (x.stdev() * conf_z_score),
            float('inf')
        ]
        if mu is None:
            if x.mean() <= y.mean():
                p = 1 - p
        else:
            if x.mean() <= mu:
                p = 1 - p
    else:
        conf_z_score = abs(norm.ppf(conf_level))
        conf_interval = [
            float('-inf'),
            x.mean() + (x.stdev() * conf_z_score)
        ]
        if mu is None:
            if x.mean() >= y.mean():
                p = 1
        else:
            if x.mean() >= mu:
                p = 1

    results["output"] = {
        't': t_score,
        'df': df,
        'p': p,
        'confidence_interval': conf_interval,
    }

    if mu is not None:
        results["output"]["mean_difference"] = mu - x.mean()
        results["output"]["mean_x"] = x.mean()
        results["output"]["mean_y"] = y.mean()
    else:
        results["output"]["mean_difference"] = y.mean() - x.mean()

    return TResult(results)

class TResult:
    """
    A ``TResult`` object will be generated and returned by t-tests. It will contain the following
    attributes:

    :TResult.desc:          A description of the t-test run (i.e. one-sample, paired-samples, etc.).
    :TResult.x:             The ``EzPyZ.Column`` object for the x column.
    :TResult.y:             The ``EzPyZ.Column`` object for the y column.
    :TResult.mu:            The population mean.
    :TResult.conf_level:    The confidence level.
    :TResult.conf_perc:     The percentage confidence level. For ``conf_level = .05``, this would be
                            ``95``.
    :TResult.t:             The t-score.
    :TResult.df:            The degrees of freedom.
    :TResult.p:             The p-value.
    :TResult.resolution:    A brief statement saying whether the null hypothesis was rejected.
    :TResult.alt:           The alternative hypothesis.
    :TResult.null:          The null hypothesis.
    :TResult.conf_interval: The confidence interval of the x column.
    :TResult.mean_diff:     The mean difference (y - x) or (μ - x).
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(self, info):
        """
        Constructs a ``TResult`` object.

        :param info:    Dictionary. The data from the t-test.
        :type info:     ``Dict[str, Union[str, Dict[str, Any]]]``
        :return:        Nothing.
        :rtype:         ``NoneType``
        """
        self.desc = info['description']
        self.x = info['options']['x']
        self.y = info['options']['y']
        self.mu = info['options']['mu']
        self.conf_level = info['options']['confidence_level']
        self.conf_perc = str((1 - self.conf_level) * 100)
        self.t = round(info['output']['t'], 4)
        self.df = round(info['output']['df'], 4)
        self.p = round(info['output']['p'], 6)
        if self.p > self.conf_level:
            self.resolution = "fail to reject null hypothesis"
        else:
            self.resolution = "reject null hypothesis"
        alt = info['options']['alternative']
        if alt == "two-tailed":
            self.alt = "true difference in means is not equal to 0"
            self.null = "true difference in means is equal to 0"
        elif alt == "less":
            self.alt = "true difference in means is less than 0"
            self.null = "true differnece in means is not less than 0"
        else:
            self.alt = "true difference in means is greater than 0"
            self.null = "true difference in means is not greater than 0"
        self.conf_int = [
            round(info['output']['confidence_interval'][0], 6),
            round(info['output']['confidence_interval'][1], 6)
        ]
        self.mean_diff = round(info['output']['mean_difference'], 6)
    def __str__(self):
        """
        Returns the ``TResult`` as a string.

        :return:    A print-friendly string representing the ``TResult`` object.
        :rtype:     ``str``

        Usage::
        
            >>> import EzPyZ as ez
            >>> data = {
            ...     'score': [15, 17, 16, 16, 19, 14, 17]
            ... }
            >>> df = ez.DataFrame(data)
            >>> # Let's conduct a two-tailed, one-sample t-test between the scores and a population
            >>> # mean, in this case well say 12.
            >>> # We'll also use the standard confidence level of 0.05.
            >>> t_res = ez.t_test(data=df, x='score', mu=15)
            >>> # t_res now contains a ``TResponse``object.
            >>> print(t_res)

                                One-sample t-test

            data:   score
            t = 7.0711, df = 6, p-value = 0.000401
            null hypothesis:                        true difference in means is equal to 0
            alternative hypothesis:                 true difference in means is not equal to 0
            resolution:                             reject null hypothesis with confidence level of 0.05
            95.0 percent confidence interval for x: [13.14278, 19.428649]
            mean of the differences (μ - x):        -4.285714

        """
        if self.mu is None:
            return ("\n\t\t\t\t\t{0}\n\n".format(self.desc) +
                    "data:\t\t\t\t\t\t\t{0} (m = {1}) ".format(self.x.title(), round(self.x.mean(), 2)) + 
                    "and {0} (m = {1})\n".format(self.y.title(), round(self.y.mean(), 2)) +
                    "output:\t\t\t\t\t\t\tt = {0}, df = {1}, p-value = {2}\n".format(self.t, self.df, self.p) +
                    "null hypothesis:\t\t\t\t\t{0}\n".format(self.null) +
                    "alternative hypothesis:\t\t\t\t\t{0}\n".format(self.alt) +
                    "resolution:\t\t\t\t\t\t{0} with confidence level of {1}\n".format(self.resolution, self.conf_level) +
                    "{0} percent confidence interval for x:\t\t\t{1}\n".format(self.conf_perc, self.conf_int) +
                    "mean of the differences (y - x):\t\t\t{0}".format(self.mean_diff)
            )
        return ("\n\t\t\t\t\t{0}\n\n".format(self.desc) +
                "data:\t\t{0} (m = {1}) and μ ({2})\n".format(self.x.title(), round(self.x.mean(), 2), self.mu) +
                "and {0} (m = {1})\n".format(self.y.title(), round(self.y.mean(), 2)) +
                "output:\t\t\t\t\t\t\tt = {0}, df = {1}, p-value = {2}\n".format(self.t, self.df, self.p) +
                "null hypothesis:\t\t\t\t\t{0}\n".format(self.null) +
                "alternative hypothesis:\t\t\t\t\t{0}\n".format(self.alt) +
                "resolution:\t\t\t\t\t\t{0} with confidence level of {1}\n".format(self.resolution, self.conf_level) +
                "{0} percent confidence interval for x:\t\t\t{1}\n".format(self.conf_perc, self.conf_int) +
                "mean of the differences (μ - x):\t{0}".format(self.mean_diff)
        )
    def __repr__(self):
        """
        Returns basic ``TResult`` information.

        :return:    Basic ``TResult`` information.
        :rtype:     ``str``

        Usage::

            >>> import EzPyZ as ez
            >>> data = {
            ...     'before': [1, 3, 4, 2, 3, 4, 6],
            ...     'after': [3, 4, 6, 9, 8, 7, 11]
            ... }
            >>> df = ez.DataFrame(data)
            >>> t_res = ez.t_test(data=df, x='before', y='after')
            >>> print(repr(t_res))
            TResult(x=before, y=after, paired=False, t=-2.9327, df=9.5647, p=0.015663)

        """
        if self.mu is None:
            return (
                "TResult(x={0}, y={1}, ".format(self.x.title(), self.y.title()) +
                "paired={0}, ".format(self.desc == "Paired t-test") +
                "t={0}, df={1}, p={2})".format(self.t, self.df, self.p)
            )
        return (
            "TResult(x={0}, μ={1}, ".format(self.x.title(), self.mu) +
            "t={0}, df={1}, p={2})".format(self.t, self.df, self.p)
        )
