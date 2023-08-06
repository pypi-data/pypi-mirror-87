import sys
import os
import re
from doxybook.doxygen import Doxygen
from doxybook.generator import Generator
from doxybook.xml_parser import XmlParser
from doxybook.cache import Cache
from doxybook.constants import Kind

def list_node(node, leval = 0):
    n = leval
    print('\t'*n, node.kind, node.name, 'now')
    if node.has_children:
        n += 1
        for child in node.children:
            print('\t'*n, child.kind, child.name, 'children')
            if child.has_children:
                list_node(child, n)

def run(output: str, 
        input: str, 
        target: str = 'gitbook',
        hints: bool = True, 
        debug: bool = True, 
        ignore_errors: bool = False,
        summary: str = None,
        allgenerator: str = None,
        doc_type = 'all',
        rel_path = '',
        ):

    os.makedirs(output, exist_ok=True)

    no_example = False
    if doc_type == 'part':
        no_example = True
    cache = Cache()
    parser = XmlParser(cache=cache, target=target, hints=hints)
    doxygen = Doxygen(input, parser, cache, doc_type = doc_type, rel_path = rel_path)
    #print('root.........................................')
    #for node in doxygen.rootnodes[0].children:
    #    print(node.name, node.kind)
    #print('groups.........................................')
    #for node in doxygen.groupsnodes[0].children:
    #    print(node.name, node.kind)
    #    if node.has_children:
    #        for child in node.children:
    #            print(node.name, node.kind)
    #sys.exit(0)
    
    #print("runing ..................................")
    #doxygen.print()
    if debug:
        doxygen.print()
    for index,v in enumerate(doxygen.index_paths):
        output_dir = os.path.join(output,os.path.basename(os.path.dirname(v)))
        if '/XML/' in v:
            xmldir = re.sub('.+/XML', '', os.path.dirname(v))
            output_dir = xmldir
            #if output_dir[0] == '/':
            #    output_dir = output_dir[1:]
            output_dir = output_dir.strip('/')
            output_dir = os.path.join(output, output_dir)
        generator = Generator(target=target, ignore_errors=ignore_errors, allgenerator=allgenerator)
        generator.functionlist(output_dir, doxygen.rootnodes[index].children)
        generator.functionlist(output_dir, doxygen.groupsnodes[index].children)
        generator.enumlist(output_dir, doxygen.groupsnodes[index].children)
        generator.definelist(output_dir, doxygen.groupsnodes[index].children)
        generator.definelist(output_dir, doxygen.rootnodes[index].children)
        generator.definelist(output_dir, doxygen.filesnodes[index].children)
        generator.typedeflist(output_dir, doxygen.groupsnodes[index].children)
        generator.typedeflist(output_dir, doxygen.rootnodes[index].children)
        generator.typedeflist(output_dir, doxygen.filesnodes[index].children)
        generator.functions(output_dir, doxygen.rootnodes[index].children)
        generator.functions(output_dir, doxygen.groupsnodes[index].children)
        generator.enums(output_dir, doxygen.rootnodes[index].children)
        generator.enums(output_dir, doxygen.groupsnodes[index].children)
        generator.annotated(output_dir, doxygen.rootnodes[index].children)
        generator.fileindex(output_dir, doxygen.filesnodes[index].children)
        generator.members(output_dir, doxygen.rootnodes[index].children)
        generator.members(output_dir, doxygen.groupsnodes[index].children)
        generator.files(output_dir, doxygen.filesnodes[index].children)
        generator.namespaces(output_dir, doxygen.rootnodes[index].children)
        generator.classes(output_dir, doxygen.rootnodes[index].children)
        generator.hierarchy(output_dir, doxygen.rootnodes[index].children)
        generator.modules(output_dir, doxygen.groupsnodes[index].children)
        generator.pages(output_dir, doxygen.pagesnodes[index].children)
        generator.relatedpages(output_dir, doxygen.pagesnodes[index].children)
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.FUNCTION, Kind.VARIABLE, Kind.TYPEDEF, Kind.ENUM], [Kind.CLASS, Kind.STRUCT, Kind.INTERFACE], 'Class Members')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.FUNCTION], [Kind.CLASS, Kind.STRUCT, Kind.INTERFACE], 'Class Member Functions')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.VARIABLE], [Kind.CLASS, Kind.STRUCT, Kind.INTERFACE], 'Class Member Variables')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.TYPEDEF], [Kind.CLASS, Kind.STRUCT, Kind.INTERFACE], 'Class Member Typedefs')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.ENUM], [Kind.CLASS, Kind.STRUCT, Kind.INTERFACE], 'Class Member Enums')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.FUNCTION, Kind.VARIABLE, Kind.TYPEDEF, Kind.ENUM], [Kind.NAMESPACE], 'Namespace Members')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.FUNCTION], [Kind.NAMESPACE], 'Namespace Member Functions')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.VARIABLE], [Kind.NAMESPACE], 'Namespace Member Variables')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.TYPEDEF], [Kind.NAMESPACE], 'Namespace Member Typedefs')
        generator.index(output_dir, doxygen.rootnodes[index].children, [Kind.ENUM], [Kind.NAMESPACE], 'Namespace Member Enums')
        generator.index(output_dir, doxygen.filesnodes[index].children, [Kind.FUNCTION], [Kind.FILE], 'Functions')
        generator.index(output_dir, doxygen.filesnodes[index].children, [Kind.DEFINE], [Kind.FILE], 'Macros')
        generator.index(output_dir, doxygen.filesnodes[index].children, [Kind.VARIABLE, Kind.UNION, Kind.TYPEDEF, Kind.ENUM], [Kind.FILE], 'Variables')

        if target == 'gitbook' and summary:
            generator.summary(output_dir, summary, \
                    doxygen.rootnodes[index].children, doxygen.groupsnodes[index].children, \
                    doxygen.filesnodes[index].children, doxygen.pagesnodes[index].children,\
                    no_example = no_example)
