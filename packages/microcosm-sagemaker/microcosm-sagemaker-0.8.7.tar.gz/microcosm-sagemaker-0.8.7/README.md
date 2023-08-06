# microcosm-sagemaker
Opinionated machine learning with SageMaker

## Usage
For best practices, see
[`cookiecutter-microcosm-sagemaker`](https://github.com/globality-corp/cookiecutter-microcosm-sagemaker).

## Profiling
Make sure `pyinstrument` is installed, either using `pip install pyinstrument` or by installing `microcosm-sagemaker` with `profiling` extra dependencies:

```
pip install -e '.[profiling]'
```

To enable profiling of the app, use the `--profile` flag with `runserver`:

```
runserver --profile
```

The service will log that it is in profiling mode and announce the directory to which it is exporting. Each call to the endpoint will be profiled and its results with be stored in a time-tagged html file in the profiling directory.

## Experiment Tracking
To use `Weights and Biases`, install `microcosm-sagemaker` with `wandb` extra depdency:

```
pip install -e '.[wandb]'
```

To enable experiment tracking in an ML repository:

* Choose the experiment tracking stores for your ML model. Currently, we only support `wandb`. To do so, add `wandb` to `graph.use()` in `app_hooks/train/app.py` and `app_hooks/evaluate/app.py`.

* Add the API key for `wandb` to the environment variables injected by Circle CI into the docker instance, by visiting `https://circleci.com/gh/globality-corp/<MODEL-NAME>/edit#env-vars` and adding `WANDB_API_KEY` as an environment variable.

* `Microcosm-sagemaker` automatically adds the config for the active bundle and its dependents to the `wandb`'s run config.

* To report a static metric:

```
class MyClassifier(Bundle):
    ...

    def fit(self, input_data):
        ...
        self.experiment_metrics.log_static(<metric_name>=<metric_value>)
```

* To report a time-series metric:

```
class MyClassifier(Bundle):
    ...

    def fit(self, input_data):
        ...
        self.experiment_metrics.log_timeseries(
            <metric_name>=<metric_value>,
            step=<step_number>
        )
```

Note that the `step` keyword argument must be provided for logging time-series.
