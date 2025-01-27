# Cookiecutter Template - FARP Stack

I've been working with a containers running FARP (FastAPI, React, Postgres) stack lately and I'm tired of the boilerplate nature and want something to automate it up for me, cue CookieCutter to the rescue.

https://cookiecutter.readthedocs.io/en/stable/

## Issues

### Issue - config lists showing up as options

This is intended. I need to nest the value or use it as something else.

I can't do this:

```json
{
  "models": ["modela", "modelb"]
}
```

This'll work, but I can't edit it from the command line when kicking off a cookiecutter template. Maybe if I do something with comma seperated values and then mess with the `pre_gen_project.py` file to convert back to a list...

```json
{
  "models": {
    "list": ["modela", "modelb"]
  }
}
```

### Issue - Loops not finding variables...

If I'm doing a loop in a file, I need to access variables from the `cookiecutter` namespace level.

This won't work:

```bash
{% for model in cookiecutter.models.list %}
http POST http://127.0.0.1:{{ ports.be }}/{{ model }}s
{% endfor %}
```

This does work:

```bash
{% for model in cookiecutter.models.list %}
http POST http://127.0.0.1:{{ cookiecutter.ports.be }}/{{ model }}s
{% endfor %}
```

### Issues - `jinja2.exceptions.TemplateSyntaxError: expected token ':', got '}'`

```plain
jinja2.exceptions.TemplateSyntaxError: expected token ':', got '}'
ERROR cookiecutter.hooks: Stopping generation because post_gen_project hook script didn't exit successfully
Hook script failed (exit status: 1)
```

I had some `{{{` in my templates. I fixed this by splitting them up like `{ {{`. They were mostly in f-strings.
