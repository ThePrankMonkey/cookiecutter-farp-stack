# Notes for {{ cookiecutter.project_name }} Backend

## Scripts

### Script - `TBD`

TBD

```bash
docker compose exec be poetry run <TBD>
```

## Play with API

### Create an entry

```bash
{% for model in cookiecutter.models.list %}
http POST http://127.0.0.1:{{ cookiecutter.ports.be }}/{{ model }}s
{% endfor %}
```

### Check the test data

```bash
{% for model in cookiecutter.models.list %}
http GET http://127.0.0.1:{{ cookiecutter.ports.be }}/{{ model }}s/1
{% endfor %}
```

### Delete Items

```bash
{% for model in cookiecutter.models.list %}
http DELETE http://127.0.0.1:{{ cookiecutter.ports.be }}/{{ model }}s/1
{% endfor %}
```

## Issues

### Issue - TBD

TBD

- https://some.link
