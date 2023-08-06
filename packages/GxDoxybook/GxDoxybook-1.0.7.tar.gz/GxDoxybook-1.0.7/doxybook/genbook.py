#!/usr/bin/env python3

import sys
import os
import re
import shutil
import argparse

class GenXML():
    def __init__(self, path, outputpath, is_server=None, path_type = 'all'):
        self.path = path #doc_path
        self.outputpath = outputpath
        if not os.path.exists(self.outputpath):
            os.system('mkdir -p '  + self.outputpath)
        #if not os.path.exists(os.path.join(self.outputpath, 'XML')):
        #    #@shutil.rmtree(os.path.join(self.outputpath, 'XML'))
        #    os.mkdir(os.path.join(self.outputpath, 'XML'))
        if not os.path.exists(os.path.join(self.outputpath, 'XML')):
            os.mkdir(os.path.join(self.outputpath, 'XML'))
        self.available_paths = {}
        self.is_server = is_server
        self.path_type = path_type

    def getdocdirs(self):
        absdocpath = os.path.join(self.path, 'doc')
        if os.path.exists(absdocpath):
            self.available_paths[os.path.basename(self.path)] = absdocpath
        else:
            modules = os.listdir(self.path)
            for module in modules:
                absdocpath = os.path.join(self.path, module, 'doc')
                if os.path.exists(absdocpath):
                    self.available_paths[module] = absdocpath

    def getmoduledoxygenconf(self,path):
        cfgdirs = []
        for dirpath,dirnames,filenames in os.walk(path):
            if self.is_server == 'yes':
                cmd = 'cd ' + dirpath + ' && git checkout . && cd -'
                os.system(cmd)
            doxygenconf = os.path.join(dirpath, 'doxygen.cfg')
            if os.path.exists(doxygenconf):
                cfgdirs.append(dirpath)
        return cfgdirs
    
    def have_no_dir_in_xml(self, targetdir, cfgdir):
        if not os.path.exists(targetdir):
            os.makedirs(targetdir)
        targetdir = re.sub('/', '\/', targetdir)

        cmd = "sed -i \'s/XML_OUTPUT \+=.\+$/XML_OUTPUT = " +\
                targetdir + '/g\' ' + cfgdir + '/doxygen.cfg'
        os.system(cmd)
        os.system('doxygen doxygen.cfg')
        no_dir = 1
        xmlpath = os.path.join(self.outputpath, 'XML')
        for i in os.listdir(xmlpath):
            path = os.path.join(xmlpath, i)
            if os.path.isdir(path):
                no_dir = 0

        os.system('rm -rf ' + xmlpath)
        return no_dir

    def getmodulexml(self, path):
        cfgdirs = self.getmoduledoxygenconf(path)
        if not cfgdirs:
            return None
        xmlpath = os.path.join(self.outputpath, 'XML')
        for cfgdir in cfgdirs:
            os.chdir(cfgdir)
            targetdir = re.sub(self.path, xmlpath, cfgdir)
            #if self.path_type == "all":
            #if os.path.basename(targetdir) == 'doc':
            #    #targetdir = re.sub('doc', '', targetdir)
            #else:
            #    targetdir = re.sub('doc/', '', targetdir)
            tmp = targetdir.split('/')
            new_tmp = []
            for i in tmp:
                if not i == 'doc':
                    new_tmp.append(i)
            targetdir = '/'.join(new_tmp)
            if not os.path.exists(targetdir):
                os.makedirs(targetdir)
            targetdir = re.sub('/', '\/', targetdir)

            cmd = "sed -i \'s/XML_OUTPUT \+=.\+$/XML_OUTPUT = " +\
                    targetdir + '/g\' ' + cfgdir + '/doxygen.cfg'
            os.system(cmd)
            os.system('doxygen doxygen.cfg')
        return cfgdirs

    def GetXml2(self):
        modules = self.getdocdirs()
        config_dirs = []
        for module, docpath in self.available_paths.items():
            cfgdirs = self.getmodulexml(docpath)
            if not cfgdirs:
                continue
            config_dirs.extend(cfgdirs)
        return self.available_paths, config_dirs

    def GetXml(self):
        self.getdocdirs()
        config_dirs = []
        if self.path_type == 'all':
            for module, docpath in self.available_paths.items():
                print(module, docpath)
                cfgdirs = self.getmodulexml(docpath)
                print(cfgdirs)
                if not cfgdirs:
                    continue
                config_dirs.extend(cfgdirs)
        elif self.path_type == 'part':
            cfgdirs = self.getmodulexml(self.path)
            config_dirs.extend(cfgdirs)
        return config_dirs

#doxybook -i xml -o book/solutiontest -s book/SUMMARY.md -t gitbook
class GenMD():
    def __init__(self, start_path, bookpath, source_paths, xmlpath, \
            path_type = 'all', link_path = '', now_dir = '', rel_path = '', enable_include_link = False):
        self.bookpath = bookpath
        self.source_paths = source_paths
        self.xmlpath = xmlpath
        self.start_path = start_path #doc_path
        self.path_type = path_type
        self.link_path = link_path
        self.exec_dir = now_dir
        self.rel_path = rel_path
        self.enable_include_link = enable_include_link
        if self.link_path.startswith('/opt/'):
            self.tmp_link_path = '/' + '/'.join(self.link_path.strip('/').split('/')[1:])

    def _check_path(self):
        if not os.path.exists(self.bookpath):
            os.makedirs(self.bookpath)

    def is_need_copy(self, path):
        for root,dirs,files in os.walk(path):
            for file_name in files:
                if 'doxygen.cfg' in file_name:
                    return False
        return True

    def copymdfile(self, path):
        #targetdir = re.sub(self.start_path,'',path)
        targetdir = os.path.relpath(path, self.start_path)
        #if self.path_type == "all":
        #if os.path.basename(path) == 'doc':
        #    targetdir = re.sub('doc','',targetdir)
        #else:
        #    targetdir = re.sub('doc/','',targetdir)
        tmp = targetdir.split('/')
        new_tmp = []
        for i in tmp:
            if not i == 'doc':
                new_tmp.append(i)
        targetdir = '/'.join(new_tmp)
        targetdir = targetdir.strip("/")
        mdfiles = os.listdir(path)
        for mdfile in mdfiles:
            if mdfile[0] == '.' or mdfile == 'doxygen.cfg':
                continue
            if mdfile == 'docs' and self.path_type == 'part':
                continue
            if os.path.isfile(os.path.join(path,mdfile)) and (mdfile.endswith('.md')\
                    or mdfile.endswith('.MD')):
                if not os.path.exists(os.path.join(self.bookpath, targetdir)):
                    os.makedirs(os.path.join(self.bookpath, targetdir))
                if mdfile == 'example.md' and self.path_type == 'all':
                    examplemd = os.path.join(path,mdfile)
                    fd = open(examplemd, 'r')
                    data = fd.read()
                    fd.close()
                    data = re.sub('^[ \t]*\n','',data)
                    if len(data) >= 3:
                        info = data.split('\n')
                        if len(info) >= 2:
                            project = info[0].lower()
                            module = info[1]
                            projects = ['gxbus','api']
                            if project in projects:
                                projectpath = os.path.join(self.start_path,\
                                        'gxtest',project)
                                cdcmd = ' cd ' + projectpath
                                buildcmd = './build config -k example -m ' + module
                                cpcmd = 'cp -f example.md ' + examplemd
                                cmd = cdcmd + ';'+ buildcmd + ';' + cpcmd
                                os.system(cmd)
                elif mdfile.endswith('.md') or mdfile.endswith('.MD'):
                    cmd = 'cp  \"' + os.path.join(path,mdfile) + '\" ' + \
                            os.path.join(self.bookpath, targetdir)
                    os.system(cmd)
            elif mdfile == 'images':
                if not os.path.exists(os.path.join(self.bookpath, targetdir)):
                    os.makedirs(os.path.join(self.bookpath, targetdir))
                cmd = 'cp -rf \"' + os.path.join(path,mdfile) + '\" ' + \
                        os.path.join(self.bookpath, targetdir)
                os.system(cmd)
            #elif self.is_need_copy(mdfile):
            #    cmd = 'cp -rf \"' + os.path.join(path,mdfile) + '\" ' + \
            #            os.path.join(self.bookpath, targetdir)
            #    os.system(cmd)
            elif os.path.isdir(os.path.join(path, mdfile)):
                self.copymdfile(os.path.join(path,mdfile))

    def delete_doc(self, in_path):
        tmp = in_path.split('/')
        new_tmp = []
        for i in tmp:
            if not i == 'doc':
                new_tmp.append(i)
        targetdir = '/'.join(new_tmp)
        targetdir = targetdir.strip("/")
        return targetdir


    def _touch_summary(self, md_dict):
        #fd.write('* [' + name + '](index.md)\n')
        summary =  os.path.join(self.bookpath, 'SUMMARY.md')
        with open(summary, 'w') as fd:
            fd.write('# Summary \n\n')
            for i in md_dict.values():
                if 'index' in i:
                    md_name = os.path.relpath(os.path.join(i['path'], 'index.md'), self.start_path)
                    md_name = self.delete_doc(md_name)
                    fd.write('* [' + md_name + '](' + md_name + ')\n')
                    if 'files' in i:
                        for f in i['files']:
                            md_name = os.path.relpath(os.path.join(i['path'], f), self.start_path)
                            md_name = self.delete_doc(md_name)
                            fd.write('  * [' + md_name + '](' + md_name + ')\n')
                else:
                    if 'files' in i:
                        for f in i['files']:
                            md_name = os.path.relpath(os.path.join(i['path'], f), self.start_path)
                            md_name = self.delete_doc(md_name)
                            fd.write('* [' + md_name + '](' + md_name + ')\n')

    def _touch_readme(self):
        readme =  os.path.join(self.bookpath, 'readme.md')
        with open(readme, 'w') as fd:
            fd.write('  ')

    def _find_all_md_path(self, in_dir):
        path_list = []
        for i in os.listdir(in_dir):
            path = os.path.join(in_dir, i)
            if os.path.isdir(path):
                pass
            else:
                if path.endswith(".md") and not path.endswith('/index.md'):
                    path_list.append(path)
        return path_list

    def before_work(self):
        self._check_path()
        md_dict = {}
        if self.path_type == 'all':
            pass
        else:
            for cfgdir in self.source_paths:
                print(cfgdir)
                #path_msg = cfgdir.split('/doc')[0].strip('/')
                path_msg = cfgdir

                md_dict[path_msg] = {
                        'path':cfgdir,
                        }
                if os.path.exists(os.path.join(cfgdir, 'index.md')):
                    md_dict[path_msg]['index'] = 'index.md'
                other_md_files = self._find_all_md_path(cfgdir)
                if len(other_md_files) > 0:
                    md_dict[path_msg]['files'] = other_md_files
            self._touch_summary(md_dict)
            self._touch_readme()

    def GenMD(self, is_all):
        self.before_work()
        if self.path_type == 'all':
            cmd = "doxybook -i " + self.xmlpath + " -o " + self.bookpath + ' -s ' + \
                self.bookpath + '/SUMMARY.md -t gitbook -a ' + is_all
        elif self.path_type == 'part':
            if self.enable_include_link:
                if self.link_path.startswith('/opt/'):
                    docref_path = os.path.join(self.tmp_link_path, self.rel_path)
                else:
                    if self.rel_path == '.':
                        docref_path = self.link_path
                    else:
                        docref_path = os.path.join(self.link_path, self.rel_path)
            else:
                docref_path = self.rel_path
            cmd = "doxybook -i " + self.xmlpath + " -o " + self.bookpath + ' -s ' + \
                self.bookpath + '/SUMMARY.md -t gitbook -a ' + is_all + ' -p part -l ' + docref_path
        print(cmd)
        print(self.link_path)
        print(self.rel_path)
        print(os.path.join(self.link_path, self.rel_path))
        print(docref_path)
        #os.exit(0)
        os.system(cmd)
        #for cfgdir in self.source_paths:
        #    self.copymdfile(cfgdir)
        self.copymdfile(self.start_path)

    def check_file(self, file_name):
        #if os.path.exists(os.path.join(self.exec_dir, self.link_path, \
        #        "_gen_output", file_name)):
        if not self.link_path.startswith('/'):
            if os.path.exists(os.path.join(self.exec_dir, self.link_path, file_name)):
                add_cmd = "cat " + os.path.join(self.bookpath, file_name) + " >> " \
                        + os.path.join(self.exec_dir, self.link_path, file_name)
                #        + os.path.join(self.exec_dir, self.link_path, "_gen_output", file_name)
                os.system(add_cmd)
            else:
                cp_cmd = "cp " + os.path.join(self.bookpath, file_name) + " " \
                        + os.path.join(self.exec_dir, self.link_path, file_name)
                        #+ os.path.join(self.exec_dir, self.link_path, "_gen_output", file_name)
                os.system(cp_cmd)
        else:
            if os.path.exists(os.path.join(self.link_path, file_name)):
                add_cmd = "cat " + os.path.join(self.bookpath, file_name) + " >> " \
                        + os.path.join(self.link_path, file_name)
                os.system(add_cmd)
            else:
                cp_cmd = "cp " + os.path.join(self.bookpath, file_name) + " " \
                        + os.path.join(self.link_path, file_name)
                os.system(cp_cmd)
    
    def modify_summary_path(self):
        summary =  os.path.join(self.bookpath, 'SUMMARY.md')
        new_summary =  os.path.join(self.bookpath, 'SUMMARY2.md')
        include_summary =  os.path.join(self.bookpath, 'include_summary.md')
        fd = open(summary, 'r')
        fn = open(new_summary, 'w')
        fi = open(include_summary, 'w')
        while 1:
            line = fd.readline()
            if not line:
                break
            if line.find('](') >= 0:
                line = line.strip('\n')
                index = line.split('[')[0]
                name = line.split('[')[1].split('](')[0]
                link = line.split('](')[1][:-1]
                if link.startswith('doc/'):
                    link = link[4:]
                n_line = index +  '[' + name + '](' + os.path.join(\
                        self.rel_path, 'book', link.strip('/')) + ')\n'
                #i_line = index +  '[' + name + '](' + os.path.join(self.link_path, '_gen_output', \
                if self.link_path.startswith('/opt/'):
                    i_line = index +  '[' + name + '](' + os.path.join(self.tmp_link_path, \
                        self.rel_path, 'book', link.strip('/')) + ')\n'
                else:
                    i_line = index +  '[' + name + '](' + os.path.join(self.link_path, \
                        self.rel_path, 'book', link.strip('/')) + ')\n'
                fn.write(n_line)
                fi.write(i_line)
            else :
                fn.write(line)
                fi.write(line)
        fd.close()
        fn.close()
        fi.close()
        mv_cmd = 'mv ' + new_summary + ' ' + summary
        os.system(mv_cmd)


def parse_options():
    parser = argparse.ArgumentParser(description='Convert doxygen XML output \
            into GitBook or Vuepress markdown output.')
    parser.add_argument('-d', '--dir',
        help='Path of module',
    )
    parser.add_argument('-t', '--type',
        help='Path Type',
    )
    parser.add_argument('-r', '--root_dir',
        help='root_dir of book, such as xxx/goxceed/v1.9-dev',
    )
    parser.add_argument('-l', '--link',
        help='doc output path',
    )
    parser.add_argument('-i', '--input', 
        type=str, 
        help='Path to doxygen goxceed folder',
    )
    parser.add_argument('-s', '--server', 
        type=str, 
        help='Run on server',
    )
    parser.add_argument('-a', '--allgenerator', 
        type=str, 
        help='Is generator all *.md in Summary',
    )
    parser.add_argument('-g', '--include', action='store_const', const = True,
        default = False,
        help='enable in include_summary'
    )


    args = parser.parse_args()

    return args


def main():
    print(sys.argv)
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parse_options()
    if args.dir != None:
        now_dir = os.getcwd()
        doc_path = args.dir
        if not doc_path.startswith('/'):
            doc_path = os.path.join(now_dir, args.dir)

        link_path = args.link
        #if not link_path.startswith('/'):
        #    link_path = os.path.join(now_dir, args.link)

        root_path = args.root_dir
        if root_path == None:
            root_path = doc_path
        elif not root_path.startswith('/'):
            root_path = os.path.join(now_dir, args.root_dir)

        if root_path != doc_path:
            if os.path.basename(root_path) == 'doc':
                root_path = re.sub('doc', '', root_path)
            else:
                root_path = re.sub('doc/', '', root_path)


        #path_type = 'all'
        #if doc_path != root_path:
        #    path_type = 'part'
        enable_include_link = args.include
        path_type = args.type

        rel_path = os.path.relpath(doc_path, root_path)
        if os.path.basename(rel_path) == 'doc':
            rel_path = re.sub('doc', '', rel_path)
        else:
            rel_path = re.sub('doc/', '', rel_path)

        doc_path = os.path.abspath(doc_path)
        #outpath = os.path.join(now_dir, link_path, '_gen_output', rel_path)
        if not link_path.startswith('/'):
            outpath = os.path.join(now_dir, link_path, rel_path)
        else:
            outpath = os.path.join(link_path, rel_path)
        os.chdir(doc_path)
        #print('link_path : ' +  link_path)
        #print('root_path : ' +  root_path)
        #print('doc_path : ' +  doc_path)
        #print('rel_path : ' + rel_path)
        #print('outpath : ' + outpath)
        print(rel_path)
        #sys.exit(0)
        genxml = GenXML(doc_path, outpath, path_type = path_type)
        cfgdirs = genxml.GetXml()
        bookoutpath = os.path.join(outpath, 'book')
        print(bookoutpath)
        genmd = GenMD(doc_path, bookoutpath, cfgdirs, outpath+'/XML', \
                path_type, link_path, now_dir, rel_path, enable_include_link)
        genmd.GenMD('yes')
        genmd.modify_summary_path()
        genmd.check_file('SUMMARY.md')
        genmd.check_file('include_summary.md')
        genmd.check_file('readme.md')
    elif args.input != None:
        doc_path = args.input
        is_server = args.server
        allgenerator = args.allgenerator
        doc_path = os.path.abspath(doc_path)
        outpath = doc_path
        outpath = os.path.join(outpath, 'docs')
        os.chdir(doc_path)
        genxml = GenXML(doc_path, outpath, is_server)
        modules, cfgdirs = genxml.GetXml2()
        if is_server == 'yes':
            for cfgdir in cfgdirs:
                os.remove(os.path.join(cfgdir,'doxygen.cfg'))
        for module, modpath in modules.items():
            if not modpath in cfgdirs:
                cfgdirs.append(modpath)
        #if is_server == 'yes':
        #    for cfgdir in cfgdirs:
        #        os.remove(os.path.join(cfgdir,'doxygen.cfg'))
        bookoutpath = os.path.join(outpath, 'book')
        genmd = GenMD(doc_path, bookoutpath, cfgdirs, outpath+'/XML' )
        genmd.GenMD(allgenerator)


if __name__ == "__main__":
    main()


#for dirpath,dirnames,filenames in os.walk(doc_path+'/gxtest/doc'):
#    print(dirpath, dirnames, filenames)
#print(os.listdir(doc_path))
#
#print(os.getcwd())
##os.chdir()
#print(doc_path)


