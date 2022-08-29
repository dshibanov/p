# projects
# put some global consts here
# or use config file maybe

import subprocess
import argparse
import os
import sys

def run(cmd):
    # print('cmd ', cmd)
    proc = subprocess.Popen(cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell=True,
    )
    stdout, stderr = proc.communicate()

    return proc.returncode, stdout, stderr


def nbs():
    rcode, stdout, stderr = run(["nb", "notebooks"])
    print(rcode)
    print(stdout)
    print(stdout.split())
    print(stderr)

def add_notebook(name):
    if notebook_exist(name) == 0:
        cmd = 'nb notebooks add ' + name
        print(cmd)
        return (run(cmd))[0]

def delete_notebook(name):
    e = notebook_exist(name)
    print(e)
    if e == 0:
        cmd = 'nb notebooks delete ' + name + ' -f'
        print('CMD: ', cmd)
        return (run(cmd))[0]

def notebook_exist(name):
    rcode, stdout, stderr = run(["nb", "notebooks", "use", name])
    print('nb_use:[rcode]: ', rcode)
    return rcode

def get_project_path(name):
    print(name)
    print(os.getenv('PROJECTS'))
    return os.getenv('PROJECTS') + '/' + name + '/'

def get_notes_path(name):
    return os.getenv('NOTES') + '/' + name + '/'

def project_exists(name):
    # if have dir with name in $PROJECTS
    if os.path.exists(get_project_path(name)) == True:
        print('project already exist')
        return 1
    return 0

def create_project(name, args=[]):
    pipfile = os.getenv('PROJECTS') +'/default/Pipfile.lock'
    if project_exists(name):
        print('ERROR: PROJECT EXIST')
        return 0

    project_path = get_project_path(name)
    notes_path = get_notes_path(name)
    os.mkdir(project_path)
    add_notebook(name)

    # add symlink
    src = notes_path
    dst = project_path + "@notes"
    os.symlink(src, dst)

    if args.template == 'default':
        os.popen(f'cp {pipfile} {project_path}')
        os.chdir(project_path)
        subprocess.run(["pipenv", "sync"])

    return 2

def do_project(name):
    # open terminator layout
    # cd to $PROJECTS/$name 
    # search tasks in nb:$name
    # open them in one window (upper) nvim

    # other parts of space should be arranged optimally for
    # working on project
    # path =  get_project_path(name)
    cmd = 'tmuxp load ' + name + ' -y'
    print(cmd)
    run(cmd)

    cmd = 'nb notebooks use ' + name
    print(cmd)
    run(cmd)
    # run('tmuxp load ' + name + ' -y')
    # print('path: ', path)
    # os.chdir(path)
    # pass

def chdir():
    run('cd /data/music')

def delete_project(name):
    # delete all entities related to project
    # ask before deleting every entity
    # are you sure want to delete 'entity_name
    cmd = 'rm -r $PROJECTS/'+name
    run(cmd)
    cmd = 'nb notebooks delete ' + name + ' -f'
    run(cmd)
    cmd = 'rm -r $HOME/.tmuxp/' + name + '.yaml'
    run(cmd)

def rename(name0, name1):
    src = os.getenv('PROJECTS') + '/'+name0
    dst = os.getenv('PROJECTS') + '/'+name1
    print(src)
    print(dst)
    os.rename(src, dst)
    cmd = 'nb notebooks rename ' + name0 + ' ' + name1
    run(cmd)
    src = os.getenv('SESSIONS') + '/'+name0
    dst = os.getenv('SESSIONS') + '/'+name1
    print(src)
    print(dst)
    os.rename(src, dst)



def layout(name, layout_type):
    # read conf file
    # open
    # find 'code' or 'normal'
    # depends on type project
    L = ["Geeks\n", "for\n", "Geeks\n"]
    # writing to file
    file1 = open('myfile.txt', 'w')
    file1.writelines(L)
    file1.close()

    file1 = open('myfile.txt', 'r')
    lines = file1.readlines()
    print(lines)

def create_layout(name):
    # open the file
    tconfig = open(os.getenv('CONFIG')+"/terminator/config",'r')
    lines = tconfig.readlines()
    count = 0

    # copy base layout here
    for line in lines:
        count += 1
        print("Line{}: {}".format(count, line))

    # paste in the end of file




def delete_layout(name):
    pass

def main():
    """ Main function. """
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--add', action='store_true')
    group.add_argument('--delete', action='store_true')
    group.add_argument('--do', action='store_true')
    group.add_argument('--rename', action='store_true')


    parser.add_argument('-t', '--template', nargs='?', const='c', default='default')

    parser.add_argument('name', type=str, nargs='?')
    parser.add_argument('name1', type=str, nargs='?')

    args = parser.parse_args()

    if args.add:
        # print(args)
        # return
        create_project(args.name, args)
    elif args.delete:
        delete_project(args.name)
    elif args.rename:
        rename(args.name, args.name1)
    elif args.do:
        do_project(args.name)

if __name__ == '__main__':
    main()

