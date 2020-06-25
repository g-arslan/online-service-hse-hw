FROM python:3-onbuild

COPY . .

CMD ["sh", "-c", "python -u db_init.py && python -u main.py"]

