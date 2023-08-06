import os
from xml.etree import ElementTree
from doxybook.node import Node
from doxybook.constants import Kind, Visibility
from doxybook.cache import Cache
from doxybook.xml_parser import XmlParser


class Doxygen:
    def __init__(self, input_path: str, parser: XmlParser, cache: Cache, \
            doc_type = 'all', rel_path = ''):
        path = os.path.join(input_path, 'index.xml')
        self.parser = parser
        self.cache = cache
        self.rootnodes = []
        self.groupsnodes =[] 
        self.filesnodes =[] 
        self.pagesnodes =[] 
        self.index_paths = []
        self.doc_type = doc_type
        self.rel_path = rel_path
        #if os.path.exists(path):
        #    self.index_paths.append(path)
        #else:
        #    dirs = os.listdir(input_path)
        #    for dir_s in dirs:
        #        dir_s = os.path.join(input_path,dir_s)
        #        if os.path.isdir(dir_s):
        #            self.index_paths.append(os.path.join(dir_s, 'index.xml'))
        self.get_index(input_path)
        print(self.index_paths)
        for path in self.index_paths:
            print('Loading Index XML from: ' + path)
            xml = ElementTree.parse(path).getroot()
            index_path = os.path.dirname(path)

            self.root = Node('root', None, self.cache, self.parser, None, \
                    doc_type = self.doc_type, rel_path = self.rel_path)
            self.groups = Node('root', None, self.cache, self.parser, None, \
                    doc_type = self.doc_type, rel_path = self.rel_path)
            self.files = Node('root', None, self.cache, self.parser, None, \
                    doc_type = self.doc_type, rel_path = self.rel_path)
            self.pages = Node('root', None, self.cache, self.parser, None, \
                    doc_type = self.doc_type, rel_path = self.rel_path)
            
            for compound in xml.findall('compound'):
                kind = Kind.from_str(compound.get('kind'))
                refid = compound.get('refid')
                if kind.is_language():
                    node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root, \
                            doc_type = self.doc_type, rel_path = self.rel_path)
                    node._visibility = Visibility.PUBLIC
                    self.root.add_child(node)
                if kind == Kind.GROUP:
                    node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root, \
                            doc_type = self.doc_type, rel_path = self.rel_path)
                    node._visibility = Visibility.PUBLIC
                    self.groups.add_child(node)
                if kind == Kind.FILE :
                #if kind == Kind.FILE or kind == Kind.DIR:
                    node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root, \
                            doc_type = self.doc_type, rel_path = self.rel_path)
                    node._visibility = Visibility.PUBLIC
                    self.files.add_child(node)
                if kind == Kind.PAGE:
                    node = Node(os.path.join(index_path, refid + '.xml'), None, self.cache, self.parser, self.root, \
                            doc_type = self.doc_type, rel_path = self.rel_path)
                    node._visibility = Visibility.PUBLIC
                    self.pages.add_child(node)

            print('Deduplicating data... (may take a minute!)')
            for i, child in enumerate(self.root.children.copy()):
                self._fix_duplicates(child, self.root, [])

            for i, child in enumerate(self.groups.children.copy()):
                self._fix_duplicates(child, self.groups, [Kind.GROUP])

            for i, child in enumerate(self.files.children.copy()):
                self._fix_duplicates(child, self.files, [Kind.FILE, Kind.DIR])

            self._fix_parents(self.files)

            print('Sorting...')
            #self._recursive_sort(self.root)
            #self._recursive_sort(self.groups)
            #self._recursive_sort(self.files)
            #self._recursive_sort(self.pages)
            self.rootnodes.append(self.root)
            self.groupsnodes.append(self.groups)
            self.filesnodes.append(self.files)
            self.pagesnodes.append(self.pages)
            #if path == "/home/gx/bbb/ccc/./XML/demuxhal/index.xml":
            #    break
            #if path == '/home/gx/bbb/ccc/./XML/deshal/index.xml':
            #    break
            #if path == '/home/gx/bbb/ccc/./XML/fehal/index.xml':
            #    break

    #def get_index(self, path):
    #    if os.path.exists(os.path.join(path,'index.xml')):
    #        self.index_paths.append(path)
    #        return
    #    else:
    #        dirs = os.listdir(path)
    #        for dir_s in dirs:
    #            dir_s = os.path.join(path,dir_s)
    #            if os.path.isdir(dir_s):
    #                if os.path.exists(os.path.join(dir_s, 'index.xml')):
    #                    self.index_paths.append(os.path.join(dir_s, 'index.xml'))
    #                else:
    #                    self.get_index(dir_s)
    def list_node(self, node, leval = 0):
        n = leval
        print('\t'*n, node.kind, node.name, 'now')
        if node.has_children:
            n += 1
            for child in node.children:
                print('\t'*n, child.kind, child.name, 'children')
                if child.has_children:
                    self.list_node(child, n)


    def get_index(self, path):
        if os.path.exists(os.path.join(path,'index.xml')):
            index_full_path = os.path.join(path, 'index.xml')
            if index_full_path not in self.index_paths:
                self.index_paths.append(index_full_path)
        dirs = os.listdir(path)
        for dir_s in dirs:
            dir_s = os.path.join(path,dir_s)
            if os.path.isdir(dir_s):
                if os.path.exists(os.path.join(dir_s, 'index.xml')):
                    index_full_path = os.path.join(dir_s, 'index.xml')
                    if index_full_path not in self.index_paths:
                        self.index_paths.append(index_full_path)
                self.get_index(dir_s)


    def _fix_parents(self, node: Node):
        if node.is_dir or node.is_root:
            for child in node.children:
                if child.is_file:
                    child._parent = node
                if child.is_dir:
                    self._fix_parents(child)

    def _recursive_sort(self, node: Node):
        node.sort_children()
        for child in node.children:
            self._recursive_sort(child)

    def _is_in_root(self, node: Node, root: Node):
        for child in root.children:
            if node.refid == child.refid:
                return True
        return False

    def _remove_from_root(self, refid: str, root: Node):
        for i, child in enumerate(root.children):
            if child.refid == refid:
                root.children.pop(i)
                return

    def _fix_duplicates(self, node: Node, root: Node, filter: [Kind]):
        for child in node.children:
            if len(filter) > 0 and child.kind not in filter:
                continue
            if self._is_in_root(child, root):
                self._remove_from_root(child.refid, root)
            self._fix_duplicates(child, root, filter)

    def print(self):
        #for node in self.root.children:
        #    self.print_node(node, '')
        #for node in self.groups.children:
        #    self.print_node(node, '')
        #for node in self.files.children:
        #    self.print_node(node, '')
        pass

    def print_node(self, node: Node, indent: str):
        print(indent, node.kind, node.name, node.url)
        #if node.kind == Kind.FUNCTION and node.name == 'libusb_interrupt_transfer':
        #    print(node.brief)
        for child in node.children:
            self.print_node(child, indent + '  ')
