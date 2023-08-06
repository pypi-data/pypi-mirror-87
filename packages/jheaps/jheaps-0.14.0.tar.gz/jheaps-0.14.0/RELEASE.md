
# Release

 1. Open `jheaps/__version__.py` and change version from `<backendversion>.<minor>.dev` to 
    `<backendversion>.<minor>` or `<backendversion>.<minor>rc1` if you are going for a 
    release candidate.

 2. Make sure docs are correctly generated. Use `cd docs && make html` and inspect the 
    output.

 3. Open `requirements/docself.txt` and change the version of jheaps. The entry should be 
    `jheaps==<backendversion>.<minor>` or similar in case of a release candidate version.

 4. Commit changes
    `git commit -m "X.X release"`

 5. Add the version number as a tag in git::

    git tag -s [-u <key-id>] jheaps-<backendversion>.<minor> -m 'signed <backendversion>.<minor> tag'

    (If you do not have a gpg key, use -m instead; it is important for
    Debian packaging that the tags are annotated)

 6. Push the new meta-data to github::

    git push --tags origin master

    (where ``origin`` is the name of the
    ``github.com:d-michail/python-jheaps`` repository.)

 7. PyPi packages will be uploaded by travis

 8. Wait until readthedocs updates the documentation.

 9. Increase the version number in `jheaps/__version__.py` and add a `dev` suffix

 10. Remove the version from `requirements/docself.txt`

 11. Commit and push changes::

    git add jheaps/__version__.py
    git add requirements/docself.txt
    git commit -m "Bump release version"
    git push origin master

 12. Done

