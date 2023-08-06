"""Convenience wrappers for dataloaders."""
from collections import defaultdict
import random
import warnings

import numpy as np
from sklearn.model_selection import ParameterGrid
from sklearn.preprocessing import LabelEncoder

from dbispipeline.base import Loader


class RepeatingLoader(Loader):
    """Repeats a specific loader a certain number of times."""

    def __init__(self, loader_class, loader_kwargs, repetitions):
        """
        Initializes the loader.

        Args:
            loader_class: Loader
                the class of the loader to be initialized
            loader_kwargs:
                the keyword arguments used to initialize the loader
            repetitions:
                how many runs should be produced
        """
        self.loader = loader_class(**loader_kwargs)
        self.repetitions = repetitions

    def load(self):
        """Loads the data."""
        for _ in range(self.repetitions):
            yield self.loader.load()

    @property
    def run_count(self):
        """Returns how many runs this loader will produce."""
        return self.repetitions

    @property
    def configuration(self):
        """DB-Representation of this loader."""
        config = self.loader.configuration
        config.update({
            'repetitions': self.repetitions,
        })
        return config


class MultiLoaderWrapper(Loader):
    """Simple wrapper sequentially yielding the result of a list of loaders."""

    def __init__(self, loaders):
        """
        Instantiates this loader.

        Args:
            loaders: a list of instantiated dataloaders.
        """
        self.loaders = loaders

    def load(self):
        """Loads the data."""
        for loader in self.loaders:
            yield loader.load()

    @property
    def run_count(self):
        """Returns how many runs this loader will produce."""
        return len(self.loaders)

    @property
    def configuration(self):
        """DB-Representation of this loader."""
        for i, loader in enumerate(self.loaders):
            yield dict(
                **loader.configuration,
                run_number=i,
                loader_class=loader.__class__.__name__,
            )


class MultiLoaderGenerator(Loader):
    """Produces a MultiLoader by specifying a range of possible parameters."""

    def __init__(self, loader_class, parameters):
        """
        Produces a MultiLoader by specifying a range of possible parameters.

        Should work similarly to the scikit parameters in a grid search.
        Args:
            loader_class: the class of the dataloader to be instantiated. Do
                not pass an instance of this class.
            parameters: If passed a list, this generator will return one
                dataloader instance for each entry in the list, and each entry
                in the list is passed to the constructor of the loader.
                If passed a dict, a grid of all combinations is generated and
                passed to the loader.
        """
        self.loaders = []
        if isinstance(parameters, dict):
            for sample in ParameterGrid(parameters):
                # this produces only dicts
                self.loaders.append(loader_class(**sample))
        else:
            for sample in parameters:
                if isinstance(sample, dict):
                    self.loaders.append(loader_class(**sample))
                else:
                    self.loaders.append(loader_class(*sample))

    def load(self):
        """Loads the data."""
        for loader in self.loaders:
            yield loader.load()

    @property
    def configuration(self):
        """DB-Representation of this loader."""
        for i, loader in enumerate(self.loaders):
            config = loader.configuration
            config['run_number'] = i
            config['class'] = loader.__class__.__name__
            yield config

    @property
    def run_count(self):
        """Returns how many runs this loader will produce."""
        return len(self.loaders)


def label_encode(cls):
    """Decorator for loaders which encodes categorical labels to integers."""
    old_load = cls.load
    old_init = cls.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        self.label_encoder = LabelEncoder()

    def new_load(self):
        data, targets = old_load(self)
        return data, self.label_encoder.fit_transform(targets)

    cls.__init__ = new_init
    cls.load = new_load
    return cls


def limiting(cls):
    """
    Decorator for loaders which constraints document and target numbers.

    This decorator can be used on a loader class to limit the amount of target
    classes as well as the amount of documents used for each of those classes.
    It adds the following arguments to the Loaders' constructor: max_targets,
    max_documents_per_target, strategy, random_seed.
    """
    old_load = cls.load
    old_init = cls.__init__

    def new_init(self,
                 *args,
                 max_targets=None,
                 max_documents_per_target=None,
                 strategy='random',
                 random_seed=None,
                 **kwargs):
        """
        Limiting loader which constraints document and target numbers.

        Args:
            max_targets: how many target classes should remain in the result.
                If set to None, all targets remain in the result.
            max_documents_per_target: how many documents should be left for
                each target class.
            strategy: how should the items that remain in the result be
                selected. Valid options are 'first' or 'random' (default).
            random_seed: Seed to provide to random.seed(). Ignored if strategy
                is set to 'first'.
        """
        old_init(self, *args, **kwargs)
        valid_strategies = ['first', 'random']
        if strategy not in valid_strategies:
            raise ValueError(f'the strategy {strategy} is not valid. Please '
                             f'choose from {valid_strategies}')
        if max_targets is not None and max_targets < 2:
            raise ValueError('max_targets must be 2 or greater')
        if max_documents_per_target is not None and \
                max_documents_per_target < 1:
            raise ValueError('max_document_per_target must be 1 or greater')

        self.max_targets = max_targets
        self.max_documents_per_target = max_documents_per_target
        self.strategy = strategy
        self.random_seed = random_seed

    def new_load(self):
        pairs = []
        if hasattr(cls, 'load_validate'):
            pairs.append(cls.load_validate(self))
        if hasattr(cls, 'load_test'):
            pairs.append(cls.load_test(self))
            pairs.append(cls.load_train(self))
        elif hasattr(cls, 'load'):
            pairs.append(old_load(self))
        else:
            raise ValueError('No loading methods found for this loader!')

        # first, restructure (x, y) pairs to {y: [x0, x1, ...]} dict
        # for each of the train, test, validate pairs
        dicts = []
        for pair in pairs:
            entry = defaultdict(list)
            for data, label in zip(pair[0], pair[1]):
                if isinstance(label, np.ndarray) or isinstance(label, list):
                    label = str(label)
                entry[label].append(data)
            dicts.append(entry)

        training_targets = set(dicts[-1].keys())
        selected_targets = _sample(values=training_targets,
                                   strategy=self.strategy,
                                   sample_limit=self.max_targets)

        result = []
        for bunch in dicts:
            bunch_result = [[], []]
            for key in selected_targets:
                values = _sample(values=bunch[key],
                                 strategy=self.strategy,
                                 sample_limit=self.max_documents_per_target)
                for value in values:
                    bunch_result[0].append(value)
                    bunch_result[1].append(key)
            result.append(bunch_result)

        if len(result) == 1:
            return result[0]
        return result

    cls.__init__ = new_init
    cls.load = new_load
    return cls


def _sample(values, strategy, sample_limit):
    if sample_limit is None:
        return list(values)

    if sample_limit >= len(values):
        warnings.warn(f'sample_limit ({sample_limit}) >= targets '
                      f'({len(values)})')
        return list(values)

    if strategy == 'first':
        return list(values)[:sample_limit]

    if strategy == 'random':
        return random.sample(values, sample_limit)
