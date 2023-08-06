
=============
Release Notes
=============

- v4.1.2

  * Adds support for multi-model accounts and passing model_id to upload

- v4.0.0

  * Add new `kazutsugi` tournament
  * Add support for new data format

- v3.7.0

  * Add concept of active and inactive tournaments
  * Remove magic numbers in data.py
  * Remove assumption that tournaments are consecutively ordered
  * Remove stake reporting
  * Remove ``history``

- v3.6.0

  * Handle 7-tournament format that begins in round 138
  * Remove ``Leaderboard`` and ``Report`` classes

- v3.5.0

  * Now works with new round 132 dataset
  * Add ``prediction.select_quantiles``
  * ``compare_data`` can now handle a dataset that changes target order
  * Silence future change warning from sklearn in ``logistic`` and
    ``logisticPCA`` models
  * Silence unit test warning on python3/linux
  * Bugfix: ``report.summary`` crashes on unresolved round

- v3.4.0

  * All reports can now handle unresolved rounds
  * Add ``report.summary``
  * Add ``report.summary_user``
  * Add ``report.whatif``
  * Add ``report.dominance``
  * Add ``report.logloss``
  * Add ``report.payout_users``
  * Replace ``round_resolution_date`` with ``round_dates`` and add open date
  * Replace ``nmr_resolution_price`` with ``nmr_round_prices`` and add open
    date and open price and add open-resolve return on nmr
  * Add unresolved rounds to ``nmr_round_prices``
  * Separate internet and analysis code in Report class
  * Add simple unit tests of report analysis code (make sure it runs)
  * Bug fixes for some reports

- v3.3.0

  * Add ``report.payout``
  * Add ``report.pass_rate``
  * Add ``report.logloss_correlation``
  * Add ``report.friends``
  * Add ``report.cutoff``
  * Remove ``get_stakes_cutoff``
  * Bugfixes in ``Report`` class
  * No longer need to specify tournament in ``get_current_round_number``

- v3.2.0

  * Complete rewrite of Report class
  * Complete rewrite of Leaderboard class

- v3.1.0

  **production, backtest, run**

  * Option to run multiple models in one function call
  * Option to run a list of arbitrary tournaments
  * Default now runs model through all five tournaments; previously no default
  * You can no longer re-name a model through the run functions
  * Bugfix: reset splitter before running

  **prediction**

  * Add ``prediction.metric_per_era``
  * Add ``prediction.drop_name`` and ``prediction.drop_tournament``
  * Rename ``prediction.drop`` to ``prediction.drop_pair``
  * ``prediction.pairs_with_name`` now accepts a list of model names
  * ``prediction.pairs_with_tournament`` now accepts a list of tournaments

  **data slicing**

  * No longer need to specify endpoints: ``data[:'era60']`` and ``data['era61':]``
  * Can now use 'eraX' as slice endpoints
  * Can now specify step size of slice: ``data['era1':'era60':2]``

  **miscellaneous**

  * Models must inhert from ``nx.Model``; it is no longer optional
  * Add ``model.name`` and ``model.rename``
  * ``download`` and ``download_deluxe`` combined into ``download``
  * ``upload`` and ``upload_deluxe`` combined into ``upload``
  * Add ``CustomSplitter``
  * Add ``CustomCVSplitter``

- v3.0.0

  * Complete redesign of Prediction class
  * Prediction object now stores tournament info
  * Predictions saved to HDF5 with old versions of numerox cannot be loaded
  * Many new features added

- v2.7.0

  * Data object can now be sliced with era names: ``data['era12':'era17']``
  * Add ``download_deluxe``
  * Add ``upload_deluxe``
  * Add ``FlipSplitter``

- v2.6.0

  * Unit tests now run on Windows
  * Add continuous integration testing on Windows with Appveyor
  * Add ``ConsecutiveCVSplitter``

- v2.5.0

  * Reorganize, edit, expand numerox's Sphinx documentation
  * Add ``prediction.summaries``
  * Reran and expanded experiments on Numerai's cross validation warning
  * You can now specify model to use when running Numerai's ``cv_warning``
  * Small improvement in unit test coverage

- v2.4.0

  * Add ``prediction.y_df``
  * Add ``get_user_activities``
  * Add ``cutoff_impact``
  * Add ``calc_cutoff``
  * Add ``model.rst``
  * Add 'ymin', 'ymean', 'ymax' options to ``prediction.metrics_per_era``
  * Update ``history``
  * Bugfix: update ``data.y_sum_hist`` for changes introduced in nx 2.3.0

- v2.3.0

  * ``data.y[tournament]`` replaces ``data.y_for_tournament(tournament)``
  * ``data.y[:]`` is equivalent to ``data.y`` from previous releases
  * Remove ``data.y1``, ``data.y2``, etc
  * Call using ``data.y_df`` instead of ``data.y_df()``
  * Internally Data object columns renamed, e.g., 'bernie' instead of y1
  * HDF Data archives created with previous releases cannot be read;
    must recreate HDF archive from Numerai zip archive
  * Update data documentation

- v2.2.0

  * Add ``get_user_names``
  * Bugfix: ``get_stakes`` cutoff confidence when it is lower than 0.1
  * Bugfix and improvements: ``data.y_similarity``
  * Replace ``data.y_correlation`` with ``data.y_df``
  * Update ``nx.history``
  * ``report.earn`` optionally do not round to nearest integer
  * ``report.stake`` now removes accounts from report that did not stake
  * ``data.__repr__`` no longer warns when all y's are missing
  * ``prediction.compare`` runs faster

- v2.1.0

  * ``show_stakes`` works with both new (round > 112) staking rules and old
  * ``get_stakes`` now works with new (round > 112) staking rules
  * Add ``get_stakes_old`` to work with old (round < 113) staking rules
  * Add ``get_stakes_users``
  * Add ``get_stakes_cutoff``
  * Bugfix: ``splitter.CheatSplitter``

- v2.0.1

  * Critical bugfix in data.y_for_tournament and data.y1, data.y2, etc
  * Bugfix: typo in Report class code

- v2.0.0

  * Redesign of numerox to support Numerai's new 5-tournament format

- v1.6.0

  * Add ``nmr_transactions``
  * Replace ``is_controlling_capital`` with ``is_stakeable``
  * ``upload`` now reports if submission is stakeable
  * Add simple unit testing of functions used by the Report class
  * Bugfix ``report.user_nmr`` corner cases such when no nmr awarded
  * Bugfix ``report.group_confidence`` corner cases such as when cumsum < $6000
  * Update readme results by using a recent Numerai dataset

- v1.5.0

  * Add ``report.user_summary``
  * Add ``report.user_nmr``
  * Add ``report.user_nmr_tax``
  * Add ``report.single_stake_payout``
  * Rename ``report.new_users`` to ``report.headcount`` and add columns

- v1.4.0

  * Add ``LoocvSplitter``
  * Add ``report.reputation``
  * Add ``report.group_confidence``
  * Add ``report.group_consistency``
  * Add ``report.group_burn``
  * Add confidence and s/c to ``Leaderboard``
  * Bugfix when sorting prediction.performance by consistency

- v1.3.0

  * Add ``report.burn``
  * Add ``report.participation``
  * Add ``report.big_staker``
  * Add ``report.new_user``
  * Add ``report.user_participation``
  * Add ``report.all``
  * Add ``history``
  * Improve ``report.earn``
  * ``Leaderboard`` now includes stake amount ``s``
  * Add utility functions ``isint`` and ``isstring``

- v1.2.0

  * Add ``Report`` class
  * Add ``Leaderboard`` class
  * Remove ``top_consistency``, ``ten99``, ``top_stakers``, ``top_earners``;
    use ``Report`` instead
  * Remove ``download_leaderboard``; use ``Leaderboard`` instead
  * Add ``get_current_round_number``
  * ``report.consistency`` now uses ln(2) as benchmark for rounds before R102;
    ties are now broken with number of rounds entered

- v1.1.0

  * Add ``load_example_predictions``
  * Add ``prediction.hash``
  * ``prediction.check`` now checks for correlation to example predictions,
    maximum absolution Z score, minimum and maximum values
  * ``example_predictions`` model now rounds to 5 decimal places
  * SciPy is now a primary dependency of numerox (not just through sklearn)

- v1.0.0

  * Add support for tournament number; defaults to current tournament #1
  * NumerAPI 0.9.0 is required
  * ``is_controlling_capital`` 58% consistency now required

- v0.9.0

  * Change log loss benchmark to 0.693 from ln(2)
  * Add the model used by Numerai to generate example_predictions.csv
  * Add ``top_consistency``
  * Add live logloss to ``download_leaderboard``
  * ``top_stakers`` now returns a dataframe
  * Use Python's decimal.Decimal to avoid staking confidence rounding errors
  * Add 'logloss_pass' and 'length' to ``prediction.metrics_per_era``
  * Add requirements.txt (thanks dhj-io)

- v0.8.0

  * ``show_stakes``: refactor, reformat output, add more options
  * ``get_stakes``: refactor, reformat output, add more options
  * Rename ``download_earnings`` to ``download_leaderboard``
  * Add ``load_prediction_csv``
  * ``tournament_number`` input variable renamed ``round_number``
  * Can now handle nmr winnings in the staking tournament: ``ten99``,
    ``top_stakers``, ``top_earners``, ``download_leaderboard``

- v0.7.0

  * Add ``top_earners``
  * Add ``round_resolution_date``
  * Add ``nmr_resolution_price`` and get prices from coinmarketcap
  * Add ``year_to_tournament_range``
  * Add more options to ``top_stakers``
  * Remove ``nmr_price`` which hard coded prices
  * ``round_number`` input variable renamed ``tournament_number``

- v0.6.0

  * Add ``ten99``
  * Add ``top_stakers``
  * Add ``download_earnings``
  * Add ``nmr_at_addr``
  * Add ``token_price_data``
  * Add ``historical_price``

- v0.5.0

  * Add ``compare_data``
  * Add ``show_stakes`` example
  * ``prediction.save`` now has an append mode
  * ``prediction.performance`` now returns a dataframe
  * ``prediction.dominance`` now returns a dataframe
  * ``prediction.summary`` now returns a dataframe
  * Remove ``prediction.performance_df``
  * Remove ``prediction.dominance_df``
  * Remove ``prediction.summary_df``
  * ``prediction.performance`` keyword changed from cols to columns
  * More prediction methods can now handle empty predictions

- v0.4.0

  * Numerox requires NumerAPI 0.8.1
  * Add ``merge_predictions``
  * Add ``prediction.check``
  * Add more columns to ``prediction.originality``
  * Add optional choice of columns in ``prediction.performance_df``
  * Column name changed to 'concord' in ``concordance`` function
  * Add example comparing performance of a single change across models
  * Add ``data.y_to_nan``
  * Bugfix: prediction.__repr__ sometimes showed wrong fraction of missing y
  * Bugfix: merging predictions with same name but different ids may fail
  * More unit tests

- v0.3.1

  * Unit test coverage 89%, up from 65%
  * Improve reporting of ``upload`` status
  * Add ``testing.HiddenPrints``
  * Bug fix: checking for equality of empty Predictions crashes
  * ``get_stakes`` informative error message when round_number < 61
  * More unit tests

- v0.3.0

  * Add ``upload`` to make submissions
  * ``download`` is the new name for ``download_dataset``
  * Add ``prediction.compare``
  * Add ``prediction.loc`` for indexing by Numerai row ids
  * Add ``prediction.rename``
  * Add ``prediction.drop``
  * ``prediction.concordance`` 3x faster when prediction contains 10 names
  * ``prediction.concordance`` now sorts by concordance
  * ``prediction.merge`` is no longer an inplace operation
  * ``prediction.merge_arrays`` is no longer an inplace operation
  * No longer take ``name`` as input: ``prediction.to_csv``,
    ``prediction.summary``, ``prediction.summary_df``
  * Remove ``model.hash``
  * Examples can now be run after installation: nx.examples.run_all_examples()
  * Redo compare_models example
  * Make more use of numerapi
  * Python package requests is no longer a dependency
  * Rewrite ``testing.micro_prediction`` for better unit testing
  * More unit tests

- v0.2.0

  * This release makes a large change to the numerox API
  * There are now 3 main classes instead of 4
  * The Report class has been merged into the Prediction class
  * The Prediction class can now hold the predictions from multiple models
  * New features have been added to the Prediction class

- v0.1.2

  * Numerox now uses (and requires) NumerAPI
  * Add file overwrite protection option to ``download_dataset``
  * Beware: ``download_dataset`` will now raise by default if file exists
  * Add ``report.__setitem__``
  * Add ``report.__contains__``
  * Add ``data.loc`` for indexing by Numerai row ids
  * Add ``report.originality``
  * Add report indexing (``report.__getitem__``)
  * More unit tests

- v0.1.1

  * Complete rewrite of all performance metrics
  * Add ``metrics_per_model``
  * Add ``report.dominance``
  * Add ``report.dominance_df``
  * Add ``prediction.performance_df``
  * Add ``mlpc`` model
  * Remove ``xgboost`` model to remove optional xgboost dependency
  * Rewrite examples of comparing performance of multiple models
  * More unit tests

- v0.1.0

  * Add ``report.correlation``
  * Add ``prediction.consistency``
  * Add ``prediction.metrics_per_era``
  * Can now specify which metrics to calculate in ``metrics_per_era``
  * Add sort_by to ``show_stakes``
  * Add ``prediction.yhatnew``
  * Add ``xgboost`` model
  * Add ``randomforest`` model
  * Add ``logisticPCA`` model
  * Models at top level: ``nx.extatrees`` instead of nx.model.extratrees, etc
  * ``logistic`` model now uses less regularization by default
  * Bugfix: display model name correctly when parameter dictionary is empty
  * More unit tests

- v0.0.9

  * Add ability to work with new (round 85) Numerai datasets
  * Update ``play_data`` with new numerai dataset
  * ``run`` now hides from your model the y you are trying to predict
  * Cumsum in ``show_stakes`` and ``get_stakes`` now dollars above you
  * ``model.hash`` combined hash of data, model name, and model parameters
  * Gentle refactor of splitters to reuse code
  * Bugfix: crash when balancing already balanced data
  * More unit tests

- v0.0.8

  * Add ``show_stakes``
  * Add ``get_stakes``
  * ``data.xnew`` is 3 times faster
  * ``data.column_list(x_only=False)`` replaces _column_list and _x_names
  * Example of Numerai's cross validation warning (hold out eras not rows)
  * Bugfix: ``data.xnew`` output didn't use contiguous memory

- v0.0.7

  * Add ``data.balance``
  * Add ``data.subsample``
  * Add ``data.hash``
  * Add ``IgnoreEraCVSplitter``
  * Add ``dataset_url`` function
  * All splitters now use a single base class
  * Add ``download_data_object`` to avoid hard coding path in examples
  * ``play_data`` is now ``data.y`` balanced
  * Rewrote ``update_play_data``
  * More unit tests

- v0.0.6

  * Add ``concordance``
  * New Runner class can run multiple models through a single data splitter
  * Update ``download_dataset`` for recent Numerai API change
  * Add ``RollSplitter`` roll forward fit-predict splits from consecutive eras
  * Add another verbosity level to ``run`` (verbosity=3)
  * Use ``play_data`` instead of numerai server or hard coding my local path
  * Bugfix: in v0.0.5 CVSplitter ran only a single cross validation fold
  * More unit tests

- v0.0.5

  * Data splitters can now be reused to run more than one model
  * To reuse a splitter, reset it: ``splitter.reset()``
  * All splitters renamed; e.g. ``cheat_splitter`` is now ``CheatSplitter``
  * Splitters are now iterator classes instead of generator functions
  * ``data.ids`` returns numpy string array copy instead of object array view
  * More unit tests

- v0.0.4

  * Add ``data.pca``
  * Add examples of transforming features
  * You can now change the number of features with ``data.xnew``
  * ``data.xnew`` is the new name of ``data.replace_x``
  * ``shares_memory`` can now check datas with different number of x columns
  * More unit tests

- v0.0.3

  * Add examples
  * Add iterator ``data.era_iter``
  * Add iterator ``data.region_iter``
  * ``prediction.ids`` and ``prediction.yhat`` are now views instead of copies
  * Remove appveyor so that unit tests can use Python's tempfile
  * Bugfix: ``prediction.copy`` was not copying the index
  * Bugfix: mistakes in two unit tests meant they could never fail
  * More unit tests

- v0.0.2

  * ``data.x`` and ``data.y`` now return fast views instead of slow copies
  * era and region stored internally as floats
  * HDF5 datasets created with v0.0.1 cannot be loaded with v0.0.2

- v0.0.1

  * Preview release of numerox
