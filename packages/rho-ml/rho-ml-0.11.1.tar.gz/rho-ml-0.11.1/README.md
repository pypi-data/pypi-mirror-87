# Rho ML

__Rho ML__ provides a _thin_, _thoughtful_, and _proven_ interface for
putting Data Science to work in production and enterprise-grade
environments. [Rho](https://rho.ai "Rho AI") uses __Rho ML__ for
workloads as varied as _NLP_, to _Computer Vision_ to
_Decision Modeling_ for professional racing. We see __Rho ML__ as
having a few key benefits.

#. __Any Model__ (_we won't dictate your libraries of choice!_)
  * Any Model with a Python interface
    * [PyTorch](https://pytorch.org/ "PyTorch")
    * [Tensorflow](https://www.tensorflow.org/ "Tensorflow")
    * [spaCy](https://spacy.io/ "spaCy")
    * [Keras](https://keras.io/ "Keras")
    * [insert your preferred library here]
    * ... or some other custom Python code
#. __Out-of-the-Box Versioning__ (_yet customizable_)
  * Versioning is a common blind-spot in data science as compared to the
    de facto standard of [Semver](https://semver.org/ "Semver") in much of
    software engineering and modern CI/CD workflows.
  * __Rho ML__ provides this _out-of-the-box_, no strings attached.
  * That said, we get that not all versioning is created equal, and provide
    easy access to customizing version patterns.
#. __Default Serialization and Deserialization__ (_yet customizable_)
  * Storing models for production workloads is non-trivial.
  * Frequently, libraries (including those listed above) provide their
  "hello world" and "quickstart" guides expecting you're on a local
  development machine with a "save to disk" type interface. __Rho ML__
  provides instant-access to easy, production-grade, methods to
  store and retrieve models.
  * The default option may not work, so __Rho ML__ provides easy
  modification as necessary for advanced use cases.
#. __Cloud and Cache__ (_speed versus cost_)
  * A "model" is not created equal with respect to production workloads.
    Storing and retrieving from the cloud versus locally (cached locally)
    makes a tremendous difference in speed and cost when dealing with models
    that often exceed 10s of megabytes / gigabytes.
  * __Rho ML__ provides a sensible default for managing storage in both
    scenarios.
#. __Shameless Plug__ (_enterprise deployments_)
  * Every __Rho ML__ model has instant compatibilty with
    [Sermos](https://sermos.ai "Sermos") for enterprise-scale deployments
    that need 10s to 10s of millions of transactions, scheduled tasks,
    models behind public APIs, or complex
    [pipelines](https://en.wikipedia.org/wiki/Directed_acyclic_graph "DAGs").

Rho ML is extremely easy to use and has only two external dependencies
[attrs](https://www.attrs.org/en/stable/ "attrs"), and

## Install

Install this software? Easy:

    pip install rho-ml

## Quickstart Guide

Here is a trivial example of a rules-based "model" implemented as a `RhoModel`,
including serialization.

    from rho_ml import RhoModel, ValidationFailedError, Version, LocalModelStorage

    class MyModel(RhoModel):

        def predict_logic(self, prediction_data):
            """ Logic for running the model on some prediction data """
            return prediction_data * 5

        def validate_prediction_input(self, prediction_data):
            """ Ensure data has an appropriate type before prediction """
            if not (isinstance(prediction_data, int)
                or isinstance(prediction_data, float)):
                raise ValidationError("Prediction data wasn't numeric!")

        def validate_prediction_output(self, data):
            """ Ensure the prediction result is between 0 and 5 """
            if not 0 <= data <= 5:
                raise ValidationError("Prediction result should always be
                between 0 and 5!")


     some_instance = MyModel(name='some_name',
                             version=Version.from_string("0.0.1"))
     result = some_instance.predict(0.5, run_validation=True)  # works!
     result_2 = some_instance.predict(10, run_validation=True)  # fails!

     local_storage = LocalModelStorage(base_path='./some-folder')
     local_storage.store(some_instance)

     stored_key = local_storage.get_key_from_pattern(model_name='some_name',
                                                     version_pattern='0.*.*')
     deserialized = local_storage.retrieve(key=stored_key)

## Core Concepts

### Rho Model

The `RhoModel` base class is the central concept in `RhoML`. A `RhoModel`
is a basic wrapper that enforces what we believe are the central tasks a
machine learning model should accomplish, provides a consistent interface
to 'all models', and provides the scaffolding for writing models that have
validated input and output.

TODO: Add additional detail on each component of a RhoModel and provide
several examples.

### Model Locator

A "model locator" in Rho ML is the combination of the _model name_, the
_model version_, and a _delimiter_ between them.

This is important for storage and retrieval of models as they evolve over
time. Using the default settings is highly recommended but each component is
configurable.

By default:

* Model names can be any alphanumeric character
* Delimeter is "_" (the underscore character)
* Model versions must adhere to [semver versioning](https://semver.org/)

e.g. `MyModel_0.1.0`

### Serialization

TODO: Describe concept of serializing/deserializing.

## Testing

To run the tests you need to have `pyenv` running on your system, along with
all python versions listed in `tox.ini` under `envlist`.

  * Install the required Python versions noted in `tox.ini`, e.g.

        pyenv install 3.7.4

Install the testing requirements locally.

    pip install -e .[test]

Now, run the tests:

    tox
