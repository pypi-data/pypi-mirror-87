# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml',
 'niaaml.classifiers',
 'niaaml.data',
 'niaaml.fitness',
 'niaaml.preprocessing',
 'niaaml.preprocessing.feature_selection',
 'niaaml.preprocessing.feature_transform',
 'niaaml.tests']

package_data = \
{'': ['*'], 'niaaml.tests': ['tests_files/*']}

install_requires = \
['NiaPy>=2.0.0rc11,<3.0.0',
 'numpy>=1.19.1,<2.0.0',
 'scikit-learn>=0.23.2,<0.24.0']

setup_kwargs = {
    'name': 'niaaml',
    'version': '0.1.2a1',
    'description': 'Python automated machine learning framework.',
    'long_description': "NiaAML\n======\n\nNiaAML is an automated machine learning Python framework based on\nnature-inspired algorithms for optimization. The name comes from the\nautomated machine learning method of the same name [1]. Its\ngoal is to efficiently compose the best possible classification pipeline\nfor the given task using components on the input. The components are\ndivided into three groups: feature seletion algorithms, feature\ntransformation algorithms and classifiers. The framework uses\nnature-inspired algorithms for optimization to choose the best set of\ncomponents for the classification pipeline on the output and optimize\ntheir parameters. We use `NiaPy framework <https://github.com/NiaOrg/NiaPy>`_ for the optimization process\nwhich is a popular Python collection of nature-inspired algorithms. The\nNiaAML framework is easy to use and customize or expand to suit your\nneeds.\n\nThe NiaAML framework allows you not only to run full pipeline optimization, but also separate implemented components such as classifiers, feature selection algorithms, etc. It currently supports only numeric features on the input. **However, we are planning to add support for categorical features too.**\n\nInstallation\n------------\n\nInstall NiaAML with pip:\n\n.. code:: sh\n\n    pip install niaaml\n\nUsage\n-----\n\nSee the project's `repository <https://github.com/lukapecnik/NiaAML>`_ for usage examples.\n\nComponents\n----------\n\nIn the following sections you can see a list of currently implemented\ncomponents divided into groups: classifiers, feature selection\nalgorithms and feature transformation algorithms. At the end you can\nalso see a list of currently implemented fitness functions for the\noptimization process.\n\nClassifiers\n~~~~~~~~~~~\n\n-  Adaptive Boosting (AdaBoost),\n-  Bagging (Bagging),\n-  Extremely Randomized Trees (ExtremelyRandomizedTrees),\n-  Linear SVC (LinearSVC),\n-  Multi Layer Perceptron (MultiLayerPerceptron),\n-  Random Forest Classifier (RandomForestClassifier).\n\nFeature Selection Algorithms\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Select K Best (SelectKBest),\n-  Select Percentile (SelectPercentile),\n-  Variance Threshold (VarianceThreshold).\n\nNature-Inspired\n^^^^^^^^^^^^^^^\n\n-  Bat Algorithm (BatAlgorithm),\n-  Differential Evolution (DifferentialEvolution),\n-  Self-Adaptive Differential Evolution (jDEFSTH),\n-  Grey Wolf Optimizer (GreyWolfOptimizer),\n-  Particle Swarm Optimization (ParticleSwarmOptimization).\n\nFeature Transformation Algorithms\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n-  Normalizer (Normalizer),\n-  Standard Scaler (StandardScaler).\n\nFitness Functions\n~~~~~~~~~~~~~~~~~\n\n-  Accuracy (Accuracy),\n-  Cohen's kappa (CohenKappa),\n-  F1-Score (F1),\n-  Precision (Precision).\n\nLicence\n-------\n\nThis package is distributed under the MIT License. This license can be\nfound online at http://www.opensource.org/licenses/MIT.\n\nDisclaimer\n----------\n\nThis framework is provided as-is, and there are no guarantees that it\nfits your purposes or that it is bug-free. Use it at your own risk!\n\nReferences\n----------\n\n[1] Iztok Fister Jr., Milan Zorman, Dušan Fister, Iztok Fister.\nContinuous optimizers for automatic design and evaluation of\nclassification pipelines. In: Frontier applications of nature inspired\ncomputation. Springer tracts in nature-inspired computing, pp.281-301,\n2020.\n",
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaAML',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
