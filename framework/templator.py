from jinja2 import Template, Environment, FileSystemLoader
from framework.settings import TEMPLATES_PATH


def render(template_name, template_path=TEMPLATES_PATH, **kwargs):
    """
    :param template_name: имя шаблона
    :param template_path: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    env = Environment()
    env.loader = FileSystemLoader(template_path)
    template = env.get_template(template_name)
    return template.render(**kwargs)
