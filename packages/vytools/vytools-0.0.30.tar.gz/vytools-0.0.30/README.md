Tools for working with vy 

**Installation and Setup**

```bash
pip install vytools
```

To take advantage of autocompletion add the following to your ~/.bashrc file 

```bash
eval "$(register-python-argcomplete vytools)"
```

**Setup**

You will need a folder to serve as the docker build context. This is a folder that all relevant code and data will go in (e.g. clone relevant repositories into this folder). Lets call this folder VYDIRECTORY (name it what you like). Add "secrets" files in VYDIRECTORY/.vy/secrets if you wish to use docker secrets. 

For example you could put an access token into a file named VY_DIRECTORY/.vy/secrets/SOME_SECRET_ACCESS_TOKEN then use vytools to build a dockerfile with this syntax:

```dockerfile
RUN --mount=type=secret,id=SOME_SECRET_ACCESS_TOKEN wget --header="Authorization: Bearer $(cat /run/secrets/SOME_SECRET_ACCESS_TOKEN)" https://some_url/some_artifact.tar.gz
```

Ultimately you should have a VYDIRECTORY that looks something like this

.
├── .vy
│   └── secrets
│       └── SOME_SECRET_ACCESS_TOKEN
│   └── jobs
│       └── ... vy will populate this folder with your runs ...
├── [other repos]
├── [other repos]
├── [other repos]


**Table of Contents**

- [Usage](#usage)

Set the vy context folder

```bash
$ vytools --root "path/to/VYDIRECTORY"
```

## History

- Test


