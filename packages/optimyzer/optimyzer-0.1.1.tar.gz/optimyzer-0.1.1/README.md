# Optimyzer

A hyperparameter optimization framework that fits into every workflow

> :warning: This project is still in _alpha_ stage. This means that interfaces might change more
often than expected. If you have any kind of issue, please drop us a line:
[info@gauss-ml.com](mailto:info@gauss-ml.com).

## Introduction

While creating machine learning models is fun, optimizing their hyperparameters usually isn't. Many
people do this manually, which is often ironically referred to as _expert descent_.

Coming more from the world of numerical optimization, many available hyperparameter optimization
frameworks see the problem as a function optimization problem. However, this means that the code of
the project has to be structured in a way that the entire machine-learning pipeline (loading data,
preprocessing, training, evaluating) is one function call. Furthermore, all parameters have to be
available as function arguments. For many projects, wrapping the entire machine learning pipeline
into a function call is cumbersome and a waste of time.

`Optimyzer` provides a framework to make hyperparameter optimization easy. It features a very simple
interface, such that the optimization can be done with just a few lines of code, and in any existing
workflow. It logs all relevant data into a file-based structure, where each experiment gets its own
folder. At the moment `Optimyzer` only uses random search because it is easy to use, highly
parallelizable and already way better than _expert descent_ or _grid search_.

If you find a bug, or have an improvement suggestion or feature request, you can directly add it
into our [issue tracker](https://gitlab.com/gauss-ml-open/optimyzer-client/-/issues). If you have
general remarks, feedback or other comments, please don't hesitate to contact us at
[info@gauss-ml.com](mailto:info@gauss-ml.com).

### Example Use-case

Let's say you want to do handwritten digit recognition on the MNIST dataset with a simple multilayer
perceptron (MLP). Already with such a setup there are a couple of parameters to tune: The depth
(number of layers) and width (units per layer) of the MLP, as well as the learning rate of the
optimization algorithm, batch size and so on. Usually there are many more. Getting those
hyperparameters right can make the difference between mediocre and world-class performance.

Sure, you can _quickly_ try out what happens when you change one of the parameters. And then tweak
another parameter. A couple of hours later, _just one more tweak and the performance will be good
enough._ We have been there. We didn't like it. With `Optimyzer`, we would like to help people to
avoid wasting their time with parameter tuning.

## Getting Started

Starting to use `Optimyzer` is really simple, as you will see from the [Installation](#installation)
and [Usage](#usage-of-the-optimyzer) sections. Additionally, we will explain how the `Optimyzer`'s
[information flow](#the-information-flow) differs from most other optimizers and how `Optimyzer`
stores the necessary data.

### Installation

Installing `Optimyzer` is very easy, just run `pip install optimyzer` in your favorite Python
environment and you're done. If you like it, you might want to add `Optimyzer` to your project's
dependencies.

By the way, `Optimyzer` does not have any dependency, it is powered by the Python Standard Library
only. Also, there is no database, no inter-process communication, nothing to install, nothing to
configure, nothing to take care of.

### Optimyzer Usage

`Optimyzer` has been built to be included in any kind of workflow as easily as possible. This is
the minimal version:

First we have to import it (of course):

```python
import optimyzer
```

Then we instantiate the `Optimyzer` object and select a directory where it runs:

```python
oy = optimyzer.Optimyzer(".")  # initializes an Optimyzer in the current workdir
```

For each parameter we want to tune, we have to tell `Optimyzer` the type and range. This is done
by adding a parameter (e.g., `IntParameter` or `FloatParameter`) to `Optimyzer`:

```python
oy.add_parameter(optimyzer.IntParameter("int_name", (minimum, maximum)))
oy.add_parameter(optimyzer.FloatParameter("float_name", (minimum, maximum)))
```

Note that the parameters can be freely named, except for the metadata names `workdir`, `id` and
`value`.

Once we have added the parameters, we can sample from the parameter space:

```python
config = oy.create_config()  # create a configuration by randomly sampling from the parameter space
```

This returns a configuration that holds all your parameters as properties, e.g., `config.int_name`
or `config.float_name`. For convenience, this configuration also contains the `id` and `workdir` of
the instance. Note that you cannot add or change your parameters after creating a configuration.

Now you can run the rest of your pipeline, using the sampled parameters from the `config`. After
everything is done and you have evaluated the `performance` of your model, you report it back to
`Optimyzer`:

```python
oy.report_loss(performance)
```

That's it already! With just a few extra lines of code, you can run your training pipeline using
hyper-parameters sampled from your search space.

You can now execute the optimization by running this file a couple of times, either sequentially in
a simple loop (if you only have one GPU) or in parallel. It doesn't matter whether you're running
this on your laptop or your GPU cluster. The only thing that you need is a shared file system where
the base directory is located.

After running this as many times as you wish, you can get the optimal configuration directly from a
static top-level function of the package:

```python
optimal_config = optimyzer.get_optimal_config(basedir)
# if Optimizer was initialized with "minimize=True", the same has to be passed here.
```

Alternatively, you can find the optimal parameters in a human-readable JSON file located at
(`best_instance/.optimyzer/config.json`), in the `basedir` you gave to `Optimyzer`.

Note that this framework is entirely transparent; there are no secret hooks for particular
libraries, nothing hidden happening. You're in control and know what is going on in your code.

#### Illustrative Integration in ML Code

A cartoon example of a machine learning pipeline based on our imaginary neural network framework
`neuralnetworks` is shown below. A full Keras tutorial is located in the [`notebooks`](notebooks)
directory, both as [cell-based script](notebooks/mnist_keras.py) and as [Jupyter
notebook](notebooks/mnist_keras.ipynb).

```python
# import stuff
import neuralnetworks as nn
import optimyzer

train_inputs, train_targets, test_inputs, test_targets = nn.load_preprocessed_data('MNIST')

# Optimyzer: initialize and configure parameterspace
oy = optimyzer.Optimyzer(".")  # initializes an Optimyzer in the current workdir

# int between 1 and 10 for the depth (number of layers)
oy.add_parameter(optimyzer.IntParameter("depth", (1, 10)))
# int between 32 and 1024 for the width (nodes per layer)
oy.add_parameter(optimyzer.IntParameter("width", (32, 1024)))  
# float between 1e-3 and 1e0 for learning_rate
oy.add_parameter(optimyzer.FloatParameter("learning_rate", (1e-3, 1e0)))  

# Optimyzer: freeze configuration and sample
config = oy.create_config()  # we create a config by randomly sampling from the parameter space

# create a model
model = nn.MLP(depth=config.depth, width=config.width)  # here we use the sampled configuration

# configure the training
opt = nn.opt.StochasticGradientDescent(model, learning_rate=config.learning_rate)

# train the model
model.train(opt, train_inputs, train_targets)

# after the training: check how many predictions were correct
pred = model.predict(test_inputs)
correct = sum(pred == test_targets)

# Optimyzer: report the loss
oy.report_loss(performance)
```

That's just four additional lines of code for using `Optimyzer`, plus one line for each parameter.

### Directory Handling

Oftentimes, machine learning pipelines write data into a working directory. For example, training
progress often is logged into a `tensorboard` directory and model checkpoints are stored as well.
`Optimyzer` therefore provides a working directory for each configuration instance, so that logging
and checkpoint saving can be done without risking to overwrite the data from other runs. `Optimyzer`
itself stores the instance configuration and resulting performance within that directory in its
`.optimyzer` folder.

#### Absolute Paths

If you already use absolute paths, great! If the path where you do your experiments is, for example,
`/var/tmp/ml-experiments/`, you can give that path directly to `optimyzer` like this:

```python
experiment_dir = "/var/tmp/ml-experiments"
oy = optimyzer.Optimyzer(experiment_dir)
```

When you create a configuration

```python
config = oy.create_config()
```

this `config` will contain a working directory `config.workdir` that you can use subsequently, for
instance to save a model

```python
model.save(os.path.join(config.workdir, "model.nn"))
```

#### Relative Paths and Current Working Directory

If you just have a script running that uses the current working directory (where the script is
executed), no problem either! You can initialize `Optimyzer` in the current working directory
as well:

```python
oy = optimyzer.Optimyzer(".")
```

When you create a configuration, you can pass the `chdir=True` switch:

```python
config = oy.create_config(chdir=True)
```

This will change the current working directory from the location of your script to the working
directory of this instance. This means that all relative file system commands are now executed
relative to the working directory. This means that you don't have to take care of the paths and can
just continue using commands that operate in the current working directory, for instance

```python
model.save("model.nn")
```

### Further Reading: How the Metadata is Stored

While `Optimyzer` works equally fine for algorithms that never store any data, it was designed to
work well with pipelines that need some kind of working directory to store results or configuration
or logging information. That's why there is one directory created for each instance. The instance
name is based on the configuration, which is hashed to generate a unique name.

This means that after executing a couple of runs, your `experiments` directory may look like this

```none
experiments
|- 5c49826a83751767729e
|- 71ae3a23d782a0465750
|- 7633242a2c695641532b
|- d0b85d53f19420d1a7a1
|- dee9fecd1f0b91346bc4
|- best_instance -> 71ae3a23d782a0465750
|- ...
```

where each directory represents one experiment instance, one configuration that has been evaluated.
The directory `best_instance` is a symbolic link that points to the directory of the best
configuration seen so far.

Each of the experiment instances contains a metadata folder `.optimyzer`, which holds the
configuration and the value of the experiment in a JSON file each

```none
experiments
|- 5c49826a83751767729e
   |- .optimyzer
       |- config.json
       |- value.json
|- 71ae3a23d782a0465750
   |- .optimyzer
       |- config.json
       |- value.json
|- ...
```
