Make your own model
===================

First take a look at the logistic regression model below:

.. code:: python

    from sklearn.linear_model import LogisticRegression
    import numerox as nx

    class logistic(nx.Model):

        def __init__(self, inverse_l2=0.0001):
            self.p = {'inverse_l2': inverse_l2}

        def fit_predict(self, dfit, dpre, tournament):
            model = LogisticRegression(C=self.p['inverse_l2'])
            model.fit(dfit.x, dfit.y[tournament])
            yhat = model.predict_proba(dpre.x)[:, 1]
            return dpre.ids, yhat

The model is just a thin wrapper around sklearn's ``LogisticRegression``. The
wrapper allows ``LogisticRegression`` to receive data from numerox and for
numerox to keep track of its predictions.

Your model must have a ``fit_predict`` method that takes three inputs: The
first is training `data`_ (``dfit``), the second is prediction data (``dpre``),
and the third is the `tournament` (integer, 1, or string, 'bernie').

The ``fit_predict`` method must return two numpy arrays. The first contains the
ids, the second the predictions. Make sure that these two arrays stay aligned!

Your model must inherit from the numerox ``Model`` class. If you optionally
place your parameters in a ``self.p`` dictionary as is done in the model above
then you will get a nice printout (model name and parameters)::

    >>> nx.production(nx.randomforest(depth=5), data)
    randomforest(max_features=2, depth=5, ntrees=100, seed=0)
    <snip>

You can also rename your model::

    >>> nx.production(nx.randomforest(depth=5).rename('rf_d5'), data)
    rf_d5(max_features=2, depth=5, ntrees=100, seed=0)
    <snip>

The current name of your model::

    >> model.name
    'rf_d5'

None of the `models in numerox`_ will likely be competitive in the Numerai
tournament. You'll have to make your own model. If you already have a model
then you can make a thin wrapper around it, as is done above, to get it to run
with numerox.

OK, now go make money!

.. _data: https://github.com/kwgoodman/numerox/blob/master/numerox/examples/data.rst
.. _models in numerox: https://github.com/kwgoodman/numerox/blob/master/numerox/model.py
