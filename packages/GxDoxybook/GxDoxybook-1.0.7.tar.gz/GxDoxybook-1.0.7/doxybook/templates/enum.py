TEMPLATE = """
### <a href="#{{node.anchor}}" id="{{node.anchor}}">{{node.kind.value}} {{node.name_long if node.is_group else node.name_short}} {{node.overload_suffix}}</a>

```cpp
{{node.codeblock}}
```

{{node.brief}}
{{node.details}}

{% if node.has_children -%}
{% for child in node.children %}
* **{{child.name}}:**  {{child.brief}}
{% endfor %}
{%- endif -%}

{% if node.reimplements %}
Implements [*{{node.reimplements.name_long}}*]({{node.reimplements.url}})
{% endif %}
"""
