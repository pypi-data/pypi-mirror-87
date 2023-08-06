import os
import sys
from getopt import getopt

def main():
    opts,args = getopt(sys.argv[1:], "i:o:")
    for k, v in opts:
        if k == '-i':
            input_file = v
        if k == '-o':
            old_file = v
    
    #old_file = 'SUMMARY.md'
    #input_file = 'doclib/include_summary.md'
    new_file = 'new_summary.md'
    
    fo = open(old_file, 'r')
    fn = open(new_file, 'w')
    
    need_insert = 0
    function_leval = -1
    function_line = ''
    addr = ''
    
    while 1:
        line = fo.readline()
        if not line:
            if need_insert == 1:
                need_insert = 0
                grep_cmd = 'cat ' + input_file + ' |grep "/' + addr + '/"'
                fd = os.popen(grep_cmd)
                msg_list = fd.readlines()
                addr = ''
                if len(msg_list) ==  0:
                    function_leval = -1
                    function_line = ''
                    fn.write(line)
                    continue
                print(function_line, end= '')
                function_line = ''
                start_leval = msg_list[0].split('* [')[0].count(' ')
                old_leval =  function_leval
                function_leval = -1
                save_leval = 0
                for i in msg_list[1:]:
                    tmp = i.split('* [')
                    tmp_leval = tmp[0].count(' ')
                    if i.find('数据结构') >=0 or i.find('函数列表') >= 0:
                        save_leval = tmp_leval
                    elif tmp_leval == save_leval:
                        continue
                    new_leval = old_leval + (tmp_leval - start_leval) - 2
                    fn.write(' '*new_leval + '* [' + tmp[1])
            break
        leval = line.split('* [')[0].count(' ')
        if leval <= function_leval and need_insert == 1:
            need_insert = 0
            grep_cmd = 'cat ' + input_file + ' |grep "/' + addr + '/"'
            fd = os.popen(grep_cmd)
            msg_list = fd.readlines()
            addr = ''
            if len(msg_list) ==  0:
                function_leval = -1
                function_line = ''
                fn.write(line)
                continue
            print(function_line, end= '')
            function_line = ''
            start_leval = msg_list[0].split('* [')[0].count(' ')
            old_leval =  function_leval
            function_leval = -1
            save_leval = 0
            for i in msg_list[1:]:
                tmp = i.split('* [')
                tmp_leval = tmp[0].count(' ')
                if i.find('数据结构') >=0 or i.find('函数列表') >= 0:
                    save_leval = tmp_leval
                elif tmp_leval == save_leval:
                    continue
                new_leval = old_leval + (tmp_leval - start_leval) - 2
                fn.write(' '*new_leval + '* [' + tmp[1])
        if line.find('功能特性') >= 0:
            fn.write(line)
            addr = os.path.dirname(line.split('book/')[1].strip('\n)'))
            need_insert = 1
            function_leval = line.split('* [')[0].count(' ')
            function_line = line
        else:
            fn.write(line)
    
    fo.close()
    fn.close()
    
    mv_cmd = 'mv ' + new_file + ' ' +  old_file
    os.system(mv_cmd)

if __name__ == "__main__":
    main()
