@echo off
CHOICE /C:01 /m "Which Repo? [1]testpypi or [0]pypi"
    goto sub_%ERRORLEVEL%

:sub_1
    echo Uploading to pypi
    pushd ..\..
    Uploading file..
    realpath dist/*.whl
    twine upload --verbose dist/*.whl
    popd
    GOTO:eof
:sub_2
    echo Uploading to testpypi
    pushd ..\..
    Uploading file..
    realpath dist/*.whl
    twine upload --verbose --repository testpypi dist/*.whl
    popd
    GOTO:eof

