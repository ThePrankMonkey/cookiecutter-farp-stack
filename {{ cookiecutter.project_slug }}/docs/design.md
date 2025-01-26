# Design - {{ cookiecutter.project_name }}

## Problem

Describe why this project exists

## Requirements

- Database
  {% for model in cookiecutter.models %}
  - {{ model|title }}
    {% endfor %}
- Frontend
- Backend

## Questions

TBD

## Design Diagrams

### Frontend

TBD

### Backend

TBD

### Database

TBD

### Scripts

TBD
