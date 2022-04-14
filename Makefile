install:
	python3 -m venv .venv && \
	.venv/bin/python -m pip install --upgrade pip && \
	.venv/bin/python -m pip install -r requirements.txt

run-gunicorn:
	FLASK_ENV=production .venv/bin/gunicorn \
	       	--bind=0.0.0.0:8181 \
		-w 1 \
		--capture-output \
		"app:gunicorn()"

run:
	.venv/bin/python app.py

clean:
	rm -rf .venv
