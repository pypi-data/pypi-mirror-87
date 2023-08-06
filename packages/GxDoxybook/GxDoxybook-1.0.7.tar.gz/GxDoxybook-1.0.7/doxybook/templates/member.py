TEMPLATE = """
# {{node.kind.value|title}} {{node.name_long}}
{% if node.has_templateparams %}
**template &lt;{{node.templateparams}}&gt;**
{% endif %}

{% if node.is_group -%}
[**Modules**](modules.md)
{% elif node.is_file or node.is_dir -%}
[**File List**](files.md)
{%- else -%}
[**Class List**](annotated.md)
{%- endif %}
{%- for parent in node.parents -%}
{{'**>**'|indent(1, true)}} [**{{parent.name_long if node.is_group else parent.name_short}}**]({{parent.url}})
{%- endfor %}

```cpp
{{node.codeblock}}
```
{% if node.is_file and node.has_programlisting -%}
[Go to the source code of this file.]({{node.url_source}})
{%- endif %}

{{node.brief}}
{%- if node.has_details -%}
[More...](#detailed-description)
{%- endif %}

{% if node.has_includes -%}
{%- for include in node.includes -%}
* `#include {{include}}`
{% endfor -%}
{%- endif %}

{% if node.has_base_classes %}
Inherits the following classes:
{%- for base in node.base_classes -%}
{%- if base is string %} {{base}}{%- else %} [{{base.name_long}}]({{base.url}}){%- endif -%}
{{ ', ' if not loop.last else '' }}
{%- endfor -%}
{%- endif %}

{% if node.has_derived_classes %}
Inherited by the following classes:
{%- for derived in node.derived_classes -%}
{%- if derived is string %} {{derived}}{%- else %} [{{derived.name_long}}]({{derived.url}}){%- endif -%}
{{ ', ' if not loop.last else '' }}
{%- endfor -%}
{%- endif %}

{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': 'Files', 'visibility': 'public', 'kinds': ['file'], 'static': False}) }}
{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': 'Directories', 'visibility': 'public', 'kinds': ['dir'], 'static': False}) }}
{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': 'Modules', 'visibility': 'public', 'kinds': ['group'], 'static': False}) }}
{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': 'Namespaces', 'visibility': 'public', 'kinds': ['namespace'], 'static': False}) }}
{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': 'Classes', 'visibility': 'public', 'kinds': ['class', 'struct', 'interface'], 'static': False}) }}

{%- for visibility in ['public', 'protected'] -%}
{%- for query in [['types', ['enum', 'union', 'typedef']], ['attributes', ['variable']], ['functions', ['function']]] -%}
{%- for static in [['', False], ['static ', True]] %}
{{ member_table_template.render({'target': target, 'node': node, 'parent': None, 'title': visibility|title + ' ' + static[0]|title + query[0]|title, 'visibility': visibility, 'kinds': query[1], 'static': static[1]}) }}
{%- for child in node.base_classes recursive -%}{%- if child is not string %}
{{ member_table_template.render({'target': target, 'node': child, 'parent': node, 'title': visibility|title + ' ' + static[0]|title + query[0]|title, 'visibility': visibility, 'kinds': query[1], 'static': static[1]}) }}
{{- loop(child.base_classes)}}
{%- endif -%}{%- endfor -%}
{%- endfor -%}
{%- endfor -%}
{%- endfor -%}


"""
