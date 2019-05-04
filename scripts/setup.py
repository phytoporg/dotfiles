#
# Run this to install all packages and pull/builld/install git packages.
#

import os
import sys
import subprocess
import shutil

home_path = os.environ['HOME']
code_path = os.path.join(home_path, 'code')
dotfiles_path = os.path.join(code_path, 'dotfiles')
setup_path = os.path.join(dotfiles_path, 'setup')
rcfiles_path = os.path.join(dotfiles_path, 'rcfiles')

setup_packages_path = os.path.join(setup_path, 'packages')
setup_github_path = os.path.join(setup_path, 'github')
setup_rcfiles_path = os.path.join(setup_path, 'rcfiles')

#
# Read sections from the setup packages and github packages paths
#
def read_sections(filename):
    with open(filename, 'r') as fr:
        setup_sections = {}
        current_section = ''
        for line in fr.readlines():
            line = line.strip()
            if line[0] == '[' and line[-1] == ']':
                current_section = line[1:-1]
                if current_section not in setup_sections:
                    setup_sections[current_section] = []
            elif line[0] == '#':
                continue
            elif len(current_section) > 0:
                setup_sections[current_section].append(line)

    return setup_sections

packages_sections = read_sections(setup_packages_path)
github_sections = read_sections(setup_github_path)
rcfiles_sections = read_sections(setup_rcfiles_path)

valid_sections = [k for k in packages_sections.keys() \
                        if k in github_sections and   \
                           k in rcfiles_sections]

if len(sys.argv) < 2 or sys.argv[1] not in valid_sections:
    print('Please select a section. Valid sections are {}'.format(', '.join(valid_sections)))
    exit()

selected_section = sys.argv[1]

#
# Install the packages
#

print("Installing packages...")
for package in packages_sections[selected_section]:
    proc = subprocess.Popen(['sudo', 'apt', 'install', package])    
    proc.wait()

#
# Clone the github projects
#
print("Cloning github projects to {}...".format(code_path))
for project in github_sections[selected_section]:
    tokens = project.split()
    project_url = 'https://github.com/{}.git'.format(tokens[0])

    args = ['git', 'clone', project_url]
    if len(tokens) > 1:
        target_dir = os.path.join(code_path, tokens[1])
        args.append(target_dir)
    else:
        project_name = tokens[0].split('/')[1]
        target_dir = os.path.join(code_path, project_name)
        args.append(target_dir)

    if os.path.exists(target_dir):
        print("{} already exists. Not cloning project {}.".format(target_dir, tokens[0]))
    else:
        proc = subprocess.Popen(args)
        proc.wait()

#
# Deploy dotfiles
# 
print("Deploying dotfiles...")
for rcfile in rcfiles_sections[selected_section]:
    tokens = rcfile.split()

    src = os.path.join(rcfiles_path, os.path.expandvars(tokens[0]))
    dst = os.path.expandvars(tokens[1])

    if os.path.exists(dst):
        os.remove(dst)

    os.symlink(src, dst)
    print("Linked {} to {}".format(src, dst))
