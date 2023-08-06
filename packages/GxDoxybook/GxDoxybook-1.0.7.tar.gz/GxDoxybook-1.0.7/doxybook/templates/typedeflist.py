TEMPLATE = """
# Typedef List

Here are the Typedefs with brief descriptions:


{% for node in nodes recursive %}
{%- if node.is_typedef  %}
{% if not node.typedefstructtype %}

* **{{node.kind.value}}** <a id=\"{{node.anchor}}\"> [**{{node.type}}**]({{node.typerefid+'.md'}}) **{{node.name_short}}** {{node.brief}}</a>

{%- endif %}
{%- endif %}
{%- if node.has_children %}
  {{- loop(node.children) }}
{%- endif -%}
{%- endfor %}
"""
#{%- if node.is_define and node.brief %}
