Hello, git!


prod run:
```
gunicorn wsgi:application \
  --bind 127.0.0.1:8000 \
  --workers 2 \
  --threads 2 \
  --log-level info \
  --access-logfile - \
  --error-logfile -
```


debug run (uncomment debug lines in index.wsgi)
```
gunicorn wsgi:application \
  --reload \
  --workers 1 \
  --log-level debug \
  --access-logfile - \
  --error-logfile -
```