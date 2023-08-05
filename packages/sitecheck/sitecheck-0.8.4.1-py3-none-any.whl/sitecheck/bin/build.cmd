@echo off
setlocal enabledelayedexpansion

set /p content=<version.txt
echo Previous upload: %content%

:query  
    
    set /P "version=Version number?"
    CHOICE /C:01 /m "Confirm version: %version%? [1]Break [0]Continue:"    
        goto sub_%ERRORLEVEL%
    
:sub_1
    echo %version% > version.txt
    pushd ..\..
    python setup.py --version %version%
    popd
    GOTO:upload
:sub_2
    echo okay
    GOTO:eof

:upload
    CHOICE /C:01 /m "Upload build? [1]Break [0]Continue:"
        goto up_%ERRORLEVEL%
        
:up_2
    GOTO:eof
:up_1
    upload.cmd
    GOTO:eof
