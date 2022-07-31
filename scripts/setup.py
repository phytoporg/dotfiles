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
scripts_path = os.path.join(dotfiles_path, 'scripts')

setup_packages_path = os.path.join(setup_path, 'packages')
setup_pipfile_path = os.path.join(setup_path, 'pip')
setup_github_path = os.path.join(setup_path, 'github')
setup_rcfiles_path = os.path.join(setup_path, 'rcfiles')
setup_scripts_path = os.path.join(setup_path, 'scripts')
setup_commands_path = os.path.join(setup_path, 'setup_commands')

#
# Read sections from the setup packages and github packages paths
#
def read_sections(filename):
    with open(filename, 'r') as fr:
        setup_sections = {}
        current_section = ''
        for line in fr.readlines():
            line = line.strip()

            if len(line) == 0 or line[0] == '#':
                continue
            elif line[0] == '[' and line[-1] == ']':
                current_section = line[1:-1]
                if current_section not in setup_sections:
                    setup_sections[current_section] = []
            elif len(current_section) > 0:
                setup_sections[current_section].append(line)

    return setup_sections

def read_sections_with_build(filename):
    with open(filename, 'r') as fr:
        setup_sections = {}
        build_instructions = {}

        current_section = ''
        last_project = ''

        in_build = False
        for line in fr.readlines():
            line = line.strip()

            if len(line) == 0 or line[0] == '#':
                continue
            elif line[0] == '[' and line[-1] == ']':
                current_section = line[1:-1]
                if current_section not in setup_sections:
                    setup_sections[current_section] = []
            elif line == 'build' and len(last_project) > 0:
                in_build = True

                if current_section not in build_instructions:
                    build_instructions[current_section] = {}

                if last_project not in build_instructions[current_section]:
                    build_instructions[current_section][last_project] = []

            elif line == 'dliub':
                if not in_build:
                    continue

                in_build = False
            elif len(current_section) > 0 and not in_build and not line in ['build', 'dliub']:
                setup_sections[current_section].append(line)
                last_project = line
            elif len(current_section) > 0 and len(last_project) > 0 and in_build and not line == 'dliub':
                build_instructions[current_section][last_project].append(line)


    return setup_sections, build_instructions

packages_sections = read_sections(setup_packages_path)
pip_sections = read_sections(setup_pipfile_path)
rcfiles_sections = read_sections(setup_rcfiles_path)
scripts_sections = read_sections(setup_scripts_path)
github_sections, build_instructions = read_sections_with_build(setup_github_path)
commands_sections = read_sections(setup_commands_path)

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
    proc = subprocess.Popen(['sudo', 'apt', 'install', package, '-y'])    
    proc.wait()

#
# Install pip packages
#

print("Installing pip packages...")
for pip_package in pip_sections[selected_section]:
    proc = subprocess.Popen(['python3', '-m', 'pip', 'install', pip_package])    
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
        expanded_path = os.path.expandvars(tokens[1])
        if not os.path.isabs(expanded_path):
            target_dir = os.path.join(code_path, expanded_path)
        else:
            target_dir = os.path.expandvars(expanded_path)
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
    # Execute build instructions if they exist
    #
    if selected_section in build_instructions and \
            project in build_instructions[selected_section]:

        os.chdir(target_dir)
        for to_execute in build_instructions[selected_section][project]:
            tokens = to_execute.split()
            if tokens[0] == 'cd':
                os.chdir(' '.join(tokens[1:]))
            else:
                try:
                    print(f"DOTFILES[{os.getcwd()}] - {' '.join(tokens)}")
                    proc = subprocess.Popen(tokens)
                    proc.wait()
                except e:
                    print(e, file=sys.stderr)

    # TODO: restore chdir state?


#
# Deploy dotfiles
# 
print("Deploying dotfiles...")
for rcfile in rcfiles_sections[selected_section]:
    tokens = [t.strip() for t in rcfile.split()]

    src = os.path.join(rcfiles_path, os.path.expandvars(tokens[0]))
    dst = os.path.expandvars(tokens[1])

    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    if os.path.exists(dst):
        os.unlink(dst)

    os.symlink(src, dst)
    print("Linked {} to {}".format(src, dst))

#
# Deploy scripts
# 
print("Deploying scripts...")
for script in scripts_sections[selected_section]:
    tokens = script.strip().split()

    src = os.path.join(scripts_path, os.path.expandvars(tokens[0]))
    dst = os.path.expandvars(tokens[1])

    dst_dir = os.path.dirname(dst)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    if os.path.exists(dst):
        os.unlink(dst)

    try:
        os.symlink(src, dst)
        print("Linked {} to {}".format(src, dst))
    except FileExistsError as e:
        print(e)

    proc = subprocess.Popen(['chmod', '+x', dst])
    proc.wait()

#
# Run commands
#
print("Running commands...")
for command in commands_sections[selected_section]:
    command = os.path.expandvars(command)

    print(f"Running {command}")
    tokens = command.split()
    if tokens[0] == 'cd':
        os.chdir(' '.join(tokens[1:]))
    else:
        proc = subprocess.Popen(command, shell=True)
        proc.wait()

