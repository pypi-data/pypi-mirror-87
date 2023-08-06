import os
import re
import string
import traceback
from typing import TextIO
from jinja2 import Template
from jinja2.exceptions import TemplateSyntaxError, TemplateError
from jinja2 import StrictUndefined
from doxybook.node import Node, DummyNode
from doxybook.constants import Kind
from doxybook.templates.annotated import TEMPLATE as ANNOTATED_TEMPLATE
from doxybook.templates.functionlist import TEMPLATE as FUNCTIONLIST_TEMPLATE
from doxybook.templates.definelist import TEMPLATE as DEFINELIST_TEMPLATE
from doxybook.templates.typedeflist import TEMPLATE as TYPEDEFLIST_TEMPLATE
from doxybook.templates.enumlist import TEMPLATE as ENUMLIST_TEMPLATE
from doxybook.templates.function import TEMPLATE as FUNCTION_TEMPLATE
from doxybook.templates.enum import TEMPLATE as ENUM_TEMPLATE
from doxybook.templates.member import TEMPLATE as MEMBER_TEMPLATE
from doxybook.templates.member_definition import TEMPLATE as MEMBER_DEFINITION_TEMPLATE
from doxybook.templates.member_table import TEMPLATE as MEMBER_TABLE_TEMPLATE
from doxybook.templates.namespaces import TEMPLATE as NAMESPACES_TEMPLATE
from doxybook.templates.classes import TEMPLATE as CLASSES_TEMPLATE
from doxybook.templates.hierarchy import TEMPLATE as HIEARARCHY_TEMPLATE
from doxybook.templates.index import TEMPLATE as INDEX_TEMPLATE
from doxybook.templates.modules import TEMPLATE as MODULES_TEMPLATE
from doxybook.templates.files import TEMPLATE as FILES_TEMPLATE
from doxybook.templates.programlisting import TEMPLATE as PROGRAMLISTING_TEMPLATE
from doxybook.templates.page import TEMPLATE as PAGE_TEMPLATE
from doxybook.templates.pages import TEMPLATE as PAGES_TEMPLATE
import sys

LETTERS = string.ascii_lowercase + '~_@'

funcname = sys._getframe().f_back.f_code.co_name 
linenumber = sys._getframe().f_back.f_lineno 

ADDITIONAL_FILES = {
    'Namespace List': 'namespaces.md',
    'Namespace Members': 'namespace_members.md',
    'Namespace Member Functions': 'namespace_member_functions.md',
    'Namespace Member Variables': 'namespace_member_variables.md',
    'Namespace Member Typedefs': 'namespace_member_typedefs.md',
    'Namespace Member Enumerations': 'namespace_member_enums.md',
    'Class Index': 'classes.md',
    'Class Hierarchy': 'hierarchy.md',
    'Class Members': 'class_members.md',
    'Class Member Functions': 'class_member_functions.md',
    'Class Member Variables': 'class_member_variables.md',
    'Class Member Typedefs': 'class_member_typedefs.md',
    'Class Member Enumerations': 'class_member_enums.md',
}

def generate_link(name, url) -> str:
    '''
    in modify summary
    '''
    return '* [' + name + '](' + url + ')\n'

class Generator:
    def __init__(self, target: str, ignore_errors: bool = False, allgenerator: str = None):
        self.target = target
        self.allgenerator = allgenerator

        on_undefined_class = None
        if not ignore_errors:
            on_undefined_class = StrictUndefined

        try: 
            self.annotated_template = Template(ANNOTATED_TEMPLATE, undefined=on_undefined_class)
            self.functionlist_template = Template(FUNCTIONLIST_TEMPLATE, undefined=on_undefined_class)
            self.definelist_template = Template(DEFINELIST_TEMPLATE, undefined=on_undefined_class)
            self.typedeflist_template = Template(TYPEDEFLIST_TEMPLATE, undefined=on_undefined_class)
            self.function_template = Template(FUNCTION_TEMPLATE, undefined=on_undefined_class)
            self.enumlist_template = Template(ENUMLIST_TEMPLATE, undefined=on_undefined_class)
            self.enum_template = Template(ENUM_TEMPLATE, undefined=on_undefined_class)
            self.member_template = Template(MEMBER_TEMPLATE, undefined=on_undefined_class)
            self.member_definition_template = Template(MEMBER_DEFINITION_TEMPLATE, undefined=on_undefined_class)
            self.member_table_template = Template(MEMBER_TABLE_TEMPLATE, undefined=on_undefined_class)
            self.namespaces_template = Template(NAMESPACES_TEMPLATE, undefined=on_undefined_class)
            self.classes_template = Template(CLASSES_TEMPLATE, undefined=on_undefined_class)
            self.hiearchy_template = Template(HIEARARCHY_TEMPLATE, undefined=on_undefined_class)
            self.index_template = Template(INDEX_TEMPLATE, undefined=on_undefined_class)
            self.modules_template = Template(MODULES_TEMPLATE, undefined=on_undefined_class)
            self.files_template = Template(FILES_TEMPLATE, undefined=on_undefined_class)
            self.programlisting_template = Template(PROGRAMLISTING_TEMPLATE, undefined=on_undefined_class)
            self.page_template = Template(PAGE_TEMPLATE, undefined=on_undefined_class)
            self.pages_template = Template(PAGES_TEMPLATE, undefined=on_undefined_class)
        except TemplateSyntaxError as e:
            raise Exception(str(e) + ' at line: ' + str(e.lineno))

    def _render(self, tmpl: Template, path: str, data: dict) -> str:
        try: 
            print('Generating', path)
            output = tmpl.render(data)

            if (not os.path.exists(os.path.dirname(path))):
                os.makedirs(os.path.dirname(path))
            with open(path, 'w+', encoding='utf-8') as file:
                file.write(output) 
        except TemplateError as e:
            raise Exception(str(e))

    def _recursive_find(self, nodes: [Node], kind: Kind):
        ret = []
        for node in nodes:
            if node.kind == kind:
                ret.append(node)
            if node.kind.is_parent():
                ret.extend(self._recursive_find(node.children, kind))
        return ret

    def _recursive_find_with_parent(self, nodes: [Node], kinds: [Kind], parent_kinds: [Kind]):
        ret = []
        for node in nodes:
            if node.kind in kinds and node.parent is not None and node.parent.kind in parent_kinds:
                ret.append(node)
            if node.kind.is_parent() or node.kind.is_dir() or node.kind.is_file():
                ret.extend(self._recursive_find_with_parent(node.children, kinds, parent_kinds))
        return ret

    def annotated(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'annotated.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.annotated_template, path, data) 

    def functionlist(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'functionlist.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.functionlist_template, path, data) 

    def definelist(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'definelist.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.definelist_template, path, data) 

    def typedeflist(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'typedeflist.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.typedeflist_template, path, data) 

    def list_node(self, node, leval = 0):
        n = leval
        print('\t'*n, node.kind, node.name, 'now')
        if node.has_children:
            n += 1
            for child in node.children:
                print('\t'*n, child.kind, child.name, 'children')
                if child.has_children:
                    self.list_node(child, n)

    def enumlist(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'enumlist.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.enumlist_template, path, data) 

    def programlisting(self, output_dir: str, node: [Node]):
        path = os.path.join(output_dir, node.refid + '_source.md')

        data = {
            'node': node,
            'target': self.target
        }
        self._render(self.programlisting_template, path, data) 

    def fileindex(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'files.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.files_template, path, data) 

    def namespaces(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'namespaces.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.namespaces_template, path, data)

    def page(self, output_dir: str, node: Node):
        path = os.path.join(output_dir, node.name + '.md')

        data = {
            'node': node,
            'target': self.target
        }
        self._render(self.page_template, path, data)

    def pages(self, output_dir: str, nodes: [Node]):
        for node in nodes:
            self.page(output_dir, node)

    def relatedpages(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'pages.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.pages_template, path, data)

    def classes(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'classes.md')

        classes = self._recursive_find(nodes, Kind.CLASS)
        classes.extend(self._recursive_find(nodes, Kind.STRUCT))
        classes.extend(self._recursive_find(nodes, Kind.INTERFACE))
        dictionary = {}

        for letter in LETTERS:
            dictionary[letter] = []

        for klass in classes:
            if klass.name_short[0] == '\\':
                dictionary[klass.name_short[1].lower()].append(klass)
            else:
                dictionary[klass.name_short[0].lower()].append(klass)


        for letter in list(dictionary):
            if len(dictionary[letter]) == 0:
                del dictionary[letter]

        data = {
            'dictionary': dictionary,
            'target': self.target
        }
        self._render(self.classes_template, path, data) 

    def _find_base_classes(self, nodes: [Node], derived: Node):
        ret = []
        for node in nodes:
            if isinstance(node, str):
                ret.append({
                    'refid': node, 
                    'derived': derived
                })
            elif node.kind.is_parent() and not node.kind.is_namespace():
                bases = node.base_classes
                if len(bases) == 0:
                    ret.append(node)
                else:
                    ret.extend(self._find_base_classes(bases, node))
        return ret

    def modules(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'modules.md')

        data = {
            'nodes': nodes,
            'target': self.target
        }
        self._render(self.modules_template, path, data) 

    def hierarchy(self, output_dir: str, nodes: [Node]):
        path = os.path.join(output_dir, 'hierarchy.md')

        classes = self._recursive_find(nodes, Kind.CLASS)
        classes.extend(self._recursive_find(nodes, Kind.STRUCT))
        classes.extend(self._recursive_find(nodes, Kind.INTERFACE))

        bases = self._find_base_classes(classes, None)
        deduplicated = {}

        for base in bases:
            if not isinstance(base, dict):
                deduplicated[base.refid] = base
                
        for base in bases:
            if isinstance(base, dict):
                if base['refid'] not in deduplicated:
                    deduplicated[base['refid']] = []
                deduplicated[base['refid']].append(base)

        deduplicated_arr = []
        for key, children in deduplicated.items():
            if isinstance(children, list):
                deduplicated_arr.append(DummyNode(
                    key,
                    list(map(lambda x: x['derived'], children)),
                    Kind.CLASS
                ))
            else:
                found: Node = None
                for klass in classes:
                    if klass.refid == key:
                        found = klass
                        break
                if found:
                    deduplicated_arr.append(found)

        data = {
            'classes': deduplicated_arr,
            'target': self.target
        }
        self._render(self.hiearchy_template, path, data) 

    def member(self, output_dir: str, node: Node):
        path = os.path.join(output_dir, node.filename)

        data = {
            'node': node,
            'target': self.target,
            'member_definition_template': self.member_definition_template,
            'member_table_template': self.member_table_template
        }
        self._render(self.member_template, path, data)

        if node.is_language or node.is_group or node.is_file or node.is_dir:
            self.members(output_dir, node.children)

    def file(self, output_dir: str, node: Node):
        path = os.path.join(output_dir, node.filename)

        data = {
            'node': node,
            'target': self.target,
            'member_definition_template': self.member_definition_template,
            'member_table_template': self.member_table_template
        }
        self._render(self.member_template, path, data)

        if node.is_file and node.has_programlisting:
            self.programlisting(output_dir, node)

        if node.is_file or node.is_dir:
            self.files(output_dir, node.children)

    def members(self, output_dir: str, nodes: [Node]):
        for node in nodes:
            if node.is_parent or node.is_group or node.is_file or node.is_dir:
                self.member(output_dir, node)

    def function(self, output_dir: str, node: Node):
        path = os.path.join(output_dir, node.refid + '.md')
        data = {
            'node': node,
            'target': self.target,
            'member_definition_template': self.member_definition_template,
            'member_table_template': self.member_table_template
        }
        
        self._render(self.function_template, path, data)

        if node.is_language or node.is_group or node.is_file or node.is_dir:
            self.functions(output_dir, node.children)


    def functions(self, output_dir: str, nodes: [Node]):
        for node in nodes:
            if node.is_parent or node.is_group or node.is_file or node.is_dir:
                if node.has_children:
                    for child in node.children:
                        if child.kind.is_function() and (child.brief or child.details):
                            self.function(output_dir, child)
            elif node.kind.is_function():
                self.function(output_dir, child)
            else:
                pass

    def enum(self, output_dir: str, node: Node):
        path = os.path.join(output_dir, node.refid + '.md')
        data = {
            'node': node,
            'target': self.target,
            'member_definition_template': self.member_definition_template,
            'member_table_template': self.member_table_template
        }
        self._render(self.enum_template, path, data)

        if node.is_language or node.is_group or node.is_file or node.is_dir:
            self.enums(output_dir, node.children)


    def enums(self, output_dir: str, nodes: [Node]):
        for node in nodes:
            if node.is_parent or node.is_group or node.is_file or node.is_dir:
                if node.has_children:
                    for child in node.children:
                        if child.kind.is_enum() and (child.brief or child.details):
                            self.enum(output_dir, child)
            elif node.kind.is_enum():
                self.enum(output_dir, child)
            else:
                pass
                #print('functions:', node.kind)
                        #else:
                        #    print(child.kind)
                        #    self.functions(output_dir, child)


    def files(self, output_dir: str, nodes: [Node]):
        for node in nodes:
            if node.is_file or node.is_dir:
                self.file(output_dir, node)

    def index(self, output_dir: str, nodes: [Node], kind_filters: Kind, kind_parents: [Kind], title: str):
        path = os.path.join(output_dir, title.lower().replace(' ', '_') + '.md')

        found_nodes = self._recursive_find_with_parent(nodes, kind_filters, kind_parents)
        dictionary = {}

        # Populate initial dictionary
        for letter in LETTERS:
            dictionary[letter] = []

        # Sort items into the dictionary
        for found in found_nodes:
            dictionary[found.name_tokens[-1][0].lower()].append(found)

        # Delete unused letters
        for letter in list(dictionary):
            if len(dictionary[letter]) == 0:
                del dictionary[letter]

        # Sort items if they have the same name
        sorted_dictionary = {}
        for letter, items in dictionary.items():
            d = {}
            for item in items:
                # The name of the item is not yet in the dictionary
                if item.name_short not in d:
                    d[item.name_short] = [item.parent]

                # If the key is already in the dictionary,
                # make sure there are no duplicates.
                # For example an overloaded constructor or function!
                # Only allow distinct parents
                else:
                    found = False
                    for test in d[item.name_short]:
                        if test.refid == item.parent.refid:
                            found = True
                            break
                    if not found:
                        d[item.name_short].append(item.parent)

            sorted_dictionary[letter] = d

        data = {
            'title': title,
            'dictionary': sorted_dictionary,
            'target': self.target
        }
        self._render(self.index_template, path, data)

    def _generate_recursive(self, f: TextIO, node: Node, level: int, diff: str):
        if node.kind.is_parent():
            f.write(' ' * level + generate_link(node.kind.value + ' ' + node.name, diff + '/' + node.refid + '.md'))
            for child in node.children:
                self._generate_recursive(f, child, level + 2, diff)

    def _generate_recursive_function(self, f: TextIO, node: Node, level: int, diff: str):
        if node.kind.is_function() and (node.brief or node.details):
            f.write(' ' * level + generate_link(node.kind.value + ' ' + node.name, diff + '/' + node.refid + '.md'))
        if node.kind.is_group():
            for child in node.children:
                self._generate_recursive_function(f, child, level + 2, diff)

    def _generate_recursive_enum(self, f: TextIO, node: Node, level: int, diff: str):
        #if node.kind.is_enum() and node.has_brief:
        if node.kind.is_enum():
            f.write(' ' * level + generate_link(node.kind.value + ' ' + node.name, diff + '/' + node.refid + '.md'))
        if node.kind.is_group():
            for child in node.children:
                self._generate_recursive_enum(f, child, level + 2, diff)

    def _generate_recursive_files(self, f: TextIO, node: Node, level: int, diff: str):
        if node.kind.is_file() or node.kind.is_dir():
            f.write(' ' * level + generate_link(node.name, diff + '/' + node.refid + '.md'))
            if node.kind.is_file():
                f.write(' ' * level + generate_link(node.name + ' source', diff + '/' + node.refid + '_source.md'))
            for child in node.children:
                self._generate_recursive_files(f, child, level + 2, diff)

    def _generate_recursive_groups(self, f: TextIO, node: Node, level: int, diff: str):
        if node.kind.is_group():
            f.write(' ' * level + generate_link(node.title, diff + '/' + node.refid + '.md'))
            for child in node.children:
                self._generate_recursive_groups(f, child, level + 2, diff)     

    def _generate_recursive_pages(self, f: TextIO, node: Node, level: int, diff: str):
        if node.kind.is_page():
            f.write(' ' * level + generate_link(node.title, diff + '/' + node.refid + '.md'))
            for child in node.children:
                self._generate_recursive_pages(f, child, level + 2, diff)     

    def summary(self, output_dir: str, summary_file: str, nodes: [Node], modules: [Node], files: [Node], pages: [Node], no_example = False):
        print('Modifying', summary_file)
        summaryDir = os.path.dirname(os.path.abspath(summary_file))
        output_path = os.path.abspath(output_dir)
        diff = output_path[len(summaryDir)+1:].replace('\\', '/')
        #link = os.path.basename(diff) + '/index.md'
        link = 'index.md'
        if diff:
            link = diff + '/index.md'

        content = []
        with open(summary_file, 'r') as f:
            content = f.readlines()

        start = None
        offset = 0
        end = None
        for i in range(0, len(content)):
            line = content[i]
            char = ''
            findlink = re.search(re.escape(link), line)
            if findlink != None:
                char = (line[findlink.start()-1])
            if start is None and (char == '/' or char == '['):
                m = re.search('\\* \\[', line)
                if m is not None:
                    start = m.start()
                    start = i
                continue
            
            if start is not None and end is None:
                if not line.startswith(' ' * (offset + 2)):
                    end = i

        if start is None:
            print('WARNING: Could not generate summary! Unable to find \"* [...](' + link + ')\" in SUMMARY.md')
            return

        if end is None:
            end = len(content)

        with open(summary_file, 'w+') as f:
            # Write first part of the file
            for i in range(0, start+1):
                f.write(content[i])

            #f.write(' ' * (offset+2) + generate_link('Related Pages', diff + '/' + 'pages.md'))
            #for node in pages:
            #    self._generate_recursive_pages(f, node, offset + 4, diff)

            #f.write(' ' * (offset+2) + generate_link('Modules', diff + '/' + 'modules.md'))
            #for node in modules:
            #    self._generate_recursive_groups(f, node, offset + 4, diff)

            line_content = content[start]
            while content[start][offset] == ' ':
                offset = offset + 1
            if offset == 0:
                while content[start][offset] == '\t':
                    offset = offset + 8
            if start+1 < len(content):
                for i in range(start+1, len(content)):
                    is_get = 0
                    line_content = content[i]
                    keywords = ('\[数据结构\]','\[宏定义\]','\[类型定义\]','\[枚举\]', '\[结构体\]', '\[函数列表\]', '\[Example\]','\[define','\[typedef','\[union','\[enum','\[struct','\[function')
                    if not line_content:
                        continue
                    for keyword in keywords:
                        if not re.findall(keyword, line_content):
                            is_get = is_get + 1
                    if is_get == len(keywords):
                        end = i
                        break

            f.write(' ' * (offset+2) + generate_link('数据结构', diff + '/' + 'annotated.md'))
            f.write(' ' * (offset+4) + generate_link('宏定义', diff + '/' + 'definelist.md'))
            f.write(' ' * (offset+4) + generate_link('类型定义', diff + '/' + 'typedeflist.md'))
            f.write(' ' * (offset+4) + generate_link('枚举', diff + '/' + 'enumlist.md'))
            for node in modules:
                if self.allgenerator != 'no':
                    self._generate_recursive_enum(f, node, offset + 6, diff)  
            f.write(' ' * (offset+4) + generate_link('结构体', diff + '/' + 'annotated.md'))
            for node in nodes:
                if self.allgenerator != 'no':
                    self._generate_recursive(f, node, offset + 6, diff)  

            f.write(' ' * (offset+2) + generate_link('函数列表', diff + '/' + 'functionlist.md'))
            for node in modules:
                if self.allgenerator != 'no':
                    self._generate_recursive_function(f, node, offset + 4, diff)  


            if no_example == False:
                f.write(' ' * (offset+2) + generate_link('Example', diff + '/' + 'example.md'))
            #for key, val in ADDITIONAL_FILES.items():
            #    f.write(' ' * (offset+2) + generate_link(key, diff + '/' + val))

            #f.write(' ' * (offset+2) + generate_link('Files', diff + '/' + 'files.md'))
            #for node in files:
            #    self._generate_recursive_files(f, node, offset + 4, diff)    

            #f.write(' ' * (offset+2) + generate_link('File Variables', diff + '/' + 'variables.md'))
            #f.write(' ' * (offset+2) + generate_link('File Functions', diff + '/' + 'functions.md'))
            #f.write(' ' * (offset+2) + generate_link('File Macros', diff + '/' + 'macros.md'))

            ## Write second part of the file
            for i in range(end, len(content)):
                f.write(content[i])
