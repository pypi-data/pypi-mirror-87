import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ai2xl',
    version='0.0.1',
    packages=['ai2xl'],
    url='https://ai2xl.github.io',
    author='ai2xl',
    author_email='info@ai2xl.com',
    description='ai2xl is a free Python library that allows using Excel for ML data preparation, zero dependency ML '
                'model deployment, model debugging, model explainability and collaboration.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=['pandas', 'numpy', 'nyoka', 'py4j', 'python-dateutil', 'SciPy', 'scikit-learn',
                      'pandas-profiling', 'sweetviz']
)