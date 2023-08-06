TEMPLATE = """
# Macro List

Here are the macros with brief descriptions:


{% for node in nodes recursive %}
{%- if node.is_define %}

* **{{node.kind.value}}** [**{{node.name_short}}**]({{node.refid+'.md'}}) {{node.brief}}

{%- endif %}
{%- if node.has_children %}
  {{- loop(node.children) }}
{%- endif -%}
{%- endfor %}
"""
#{%- if node.is_define and node.brief %}
