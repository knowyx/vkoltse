[![Pylint](https://github.com/knowyx/vkoltse/actions/workflows/pylint.yml/badge.svg)](https://github.com/knowyx/vkoltse/actions/workflows/pylint.yml)

<img src="/static/img/logo.svg" alt="Логотип проекта" width="200" height="200">

Образование в кольце — это проект, созданный учениками учениками 10 класса, чтобы сохранить память о подвиге, совершенном нашими предками. 
Проект находится на стадии разработки.
Наши домены:
```
vkoltse.ru
вкольце.рф
www.vkoltse.ru
www.вкольце.рф
```

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
