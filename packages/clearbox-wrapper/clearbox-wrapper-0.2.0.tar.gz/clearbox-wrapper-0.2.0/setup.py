# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clearbox_wrapper']

package_data = \
{'': ['*']}

install_requires = \
['mlflow>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'clearbox-wrapper',
    'version': '0.2.0',
    'description': 'An agnostic wrapper for the most common frameworks of ML models.',
    'long_description': "# Clearbox Wrapper\n\n\nClearbox Wrapper is an agnostic wrapper for the most used machine learning frameworks, with the aim to facilitate the transfer of models between different cloud environments and to provide a common interface for generating output predictions.\n\n## Usage\n\nWith a few lines of code it is possible to create a wrapper for your model, simply specifying how to perform a prediction and how to carry out input preprocessing operations if necessary.\n\nFor example, if you have just trained a model using Sklearn and your input doesn't need preprocessing, just define a class that inherits from SklearnWrapper and specify how to perform the predict method. After that, it will be sufficient to use the Sklearn wrapper _dump_ method to have your model serialized on the disk.\n\n\n```python\nfrom sklearn.linear_model import LinearRegression\n\n...\n\nlr = lr = LinearRegression()\nlr.fit(X_train, y_train)\n\n...\n\nfrom clearbox_wrapper.SklearnWrapper import SklearnWrapper\n\nclass MyModel(SklearnWrapper):    \n    def predict(self, X):\n        return self.model.predict(X)\n\nMyModel(lr).dump('sklearn_boston.model')\n```\n\nAt this point you can move the newly created file to any environment you want and simply deserialize it to be able to use it.\n\n```python\nfrom clearbox_wrapper.SklearnWrapper import SklearnWrapper\n\nfoo = SklearnWrapper.load('sklearn_boston.model')\nfoo.predict(data)\n```\n\n## Examples\n\n#### Sklearn\n\n* Boston Housing Dataset - [Notebook](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/sklearn/sklearn_boston_dataset.ipynb)\n\n#### XGBoost\n\n* Pima Indians Diabetes - [Notebook](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/xgboost/xgboost_diabetes_dataset.ipynb) \n\n#### PyTorch\n\n* CIFAR-10 - [Notebook](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/pytorch/pytorch_cifar10_dataset.ipynb)\n\n#### Keras\n\n* Fashion MNIST - [Notebook](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/examples/keras/keras_fashion_mnist_dataset.ipynb)\n\n## License\n\n[Apache License 2.0](https://github.com/Clearbox-AI/clearbox-wrapper/blob/master/LICENSE)\n",
    'author': 'Clearbox AI',
    'author_email': 'info@clearbox.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://clearbox.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
