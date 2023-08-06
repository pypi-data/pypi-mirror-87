TEMPLATE = """
# Enum List

Here are the enums with brief descriptions:


{% for node in nodes recursive %}
{%- if node.is_enum and (node.brief or node.details) %}
* **{{node.kind.value}}** [**{{node.name_short}}**]({{node.refid+'.md'}}) {{node.brief}}
{%- endif %}
{%- if node.has_children %}
  {{- loop(node.children) }}
{%- endif -%}
{%- endfor %}
"""
