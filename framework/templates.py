import os
from jinja2 import Template
from framework.settings import TEMPLATES_PATH


def render(template_name, folder=TEMPLATES_PATH, **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    file_path = os.path.join(folder, template_name)
    with open(file_path, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)
