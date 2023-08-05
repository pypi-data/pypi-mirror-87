@echo off
CHOICE /C:01 /m "Which Repo? [1] test-Pypi or [0] Pypi"
    goto sub_%ERRORLEVEL%

:sub_1
    echo Uploading to pypi
    pushd ..\..
    echo Using wheel file:
    realpath dist/*.whl
    twine upload --verbose dist/*.whl
    rm -rf build
    rm -rf dist
    rm -rf sitecheck.egg-info
    popd    
    GOTO:eof
:sub_2
    echo Uploading to testpypi
    pushd ..\..
    Uploading file..
    realpath dist/*.whl
    twine upload --verbose --repository testpypi dist/*.whl
    rm -rf build
    rm -rf dist
    rm -rf sitecheck.egg-info
    popd
    GOTO:eof

