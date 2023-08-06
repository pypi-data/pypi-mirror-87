TEMPLATE = """
### <a href="#{{node.anchor}}" id="{{node.anchor}}">{{node.kind.value}} {{node.name_long if node.is_group else node.name_short}} {{node.overload_suffix}}</a>

```cpp
{{node.codeblock}}
```
{% if node.has_brief -%}
{{node.brief}}
{%- endif -%}

{% if node.has_details -%}
{{node.details}}
{%- endif -%}

{% if node.reimplements %}
Implements [*{{node.reimplements.name_long}}*]({{node.reimplements.url}})
{% endif %}
"""
#"\n"
