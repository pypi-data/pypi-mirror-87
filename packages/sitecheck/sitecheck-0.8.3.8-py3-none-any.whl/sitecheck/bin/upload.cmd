@echo off
CHOICE /C:01 /m "Which Repo? [1]testpypi or [0]pypi"
    goto sub_%ERRORLEVEL%
Sitecheck\dist"
:sub_1
    echo Uploading to pypi
    cd ..
    cd ..
    twine upload --verbose dist/*.whl
    GOTO:eof
:sub_2
    echo Uploading to testpypi
    cd ..
    cd ..
    twine upload --verbose --repository testpypi dist/*.whl
    GOTO:eof

