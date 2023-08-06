# quant_analytics_flow
Quantitative Analytics using Tensorflow and machine learning. Full API documentation here

https://quant-analytics-flow.readthedocs.io/


# Install package

pip install -e .
python setup.py bdist_wheel

## Run the tests

pytest --cov-report term --cov=quant_analytics_flow tests/ --html=./test-reports/report.html --cov-report=html:./test-reports/coverage --profile

## Upload Python package

python -m twine upload dist/*