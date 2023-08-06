TEMPLATE = """
# Funtion List

Here are the functions with brief descriptions:


{% for node in nodes recursive %}
{%- if node.is_function and (node.has_brief or node.has_details) %}
* **{{node.kind.value}}** [**{{node.name_short}}**]({{node.refid+'.md'}}) {{node.brief}}
{%- endif %}
{%- if node.has_children %}
  {{- loop(node.children) }}
{%- endif -%}
{%- endfor %}
"""
