import os


def get_readme_template(project_name):
    txt = '''\
# momo_PJ_name #

!!project description.

### Nitrogen Job Template ###
```
{
    "name":"momo_PJ_name",
    "description":"!!project description.",
    "docker_image":"!!docker images",
    "git_url":"!!git url",
    "git_branch":"master",
    "project":"!!project id",
    "datasets":"",
    "command":"!!run command",
    "use_gpu":0,
    "env":{"!!env":"!!default value"},
    "resource":
    {
    "spot": false,
    "cpu": 1,
    "memory": 1,
    "gpu": 0,
    "gpu_model": "standard"
    }
}
```

### Parameters ###
- `!!env`: !!type, default=!!default value. !!explanation

### Input & Output ###
Input:
- `!!file_name`  # !!comments

Output:
```
└── output
    ├── !!file_name_1  # !!comments
    └── !!file_name_2  # !!comments
```

### Maintainer ###

! your email address.

'''
    return txt.replace('momo_PJ_name', project_name)
