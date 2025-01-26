import os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("./"))


def write_model_files():
    models = "{{ cookiecutter.models }}"
    files = [
        "__init__.py",
        "model.py",
        "route.py",
    ]

    for model in models:
        model_folder = f"services/be/app/models/{model}"
        # create model folder
        os.mkdir(model_folder)
        # create model files
        data = {
            "model": model,
        }
        for file in files:
            with open(f"{model_folder}/{model}", "w") as f_obj:
                template = env.get_template(f"{{file}}.jinja")
                rendered_file = template.render(data)
                f_obj.write(rendered_file)


if __name__ == "__main__":
    write_model_files()
