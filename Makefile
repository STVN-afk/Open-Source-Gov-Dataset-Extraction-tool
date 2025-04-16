install:
	pip install -r requirements.txt

setup-dirs:
	mkdir -p downloads
	mkdir -p .csvs

run:
	python src/dataset_scripts/payment_practices.py

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

format:
	black .
