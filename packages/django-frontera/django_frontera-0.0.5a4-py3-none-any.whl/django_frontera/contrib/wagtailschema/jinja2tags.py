import jinja2.ext

from wagtailschemaorg.templatetags.wagtailschemaorg_tags import ld_print_entity, \
  ld_for_object, ld_for_site


class SchemaORGExtension(jinja2.ext.Extension):
    def __init__(self, environment):
        super(SchemaORGExtension, self).__init__(environment)
        environment.globals["ld_print_entity"] = jinja2.contextfunction(ld_print_entity)
        environment.globals["ld_for_object"] = jinja2.contextfunction(ld_for_object)
        environment.globals["ld_for_site"] = jinja2.contextfunction(ld_for_site)
