import os
from MOMORING.modules.create import create_dir, create_python_package, create_file
from MOMORING.modules.files.main_template import get_main_template
from MOMORING.modules.files.nitrogen_utils import nitrogen_utils
from MOMORING.modules.files.git_ignore_template import get_git_ignore_template
from MOMORING.modules.files.readme_template import get_readme_template
from MOMORING.modules.files.applications_template import get_applications_template


def create_project_dir(project_name):
    base_proj_name = os.path.basename(project_name)
    outer_dir = project_name.replace(base_proj_name, base_proj_name.lower())
    create_dir(outer_dir)
    os.chdir(outer_dir)

    project_name = os.path.basename(project_name)
    create_python_package(project_name)

    dirs = ['applications', 'api', 'modules', 'utils']
    for i in dirs:
        create_python_package(os.path.join(project_name, i))

    nitrogen_utils_path = os.path.join(project_name,
                                       'utils',
                                       'nitrogen_utils.py')
    create_file(nitrogen_utils_path, txt=nitrogen_utils())
    applications_file_path = os.path.join(project_name,
                                          'applications',
                                          'nitrogen_template.py')
    create_file(applications_file_path, txt=get_applications_template(project_name))
    create_file('main.py', txt=get_main_template())
    create_file('.gitignore', txt=get_git_ignore_template())
    create_file('README.md', txt=get_readme_template(project_name))
