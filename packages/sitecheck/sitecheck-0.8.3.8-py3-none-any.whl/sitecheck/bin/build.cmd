@echo off
setlocal enabledelayedexpansion

set /p content=<version.txt
echo Previous upload: %content%

:query  
    
    set /P "version=Version number? 0.8.3.:"
    CHOICE /C:01 /m "Upload %version%? [0]No, [1]Yes"    
        goto sub_%ERRORLEVEL%
    
:sub_2
    cd ..
    cd ..
    echo %version% > version.txt
    realpath %CD%
    python setup.py --version 0.8.3.%version%
    GOTO:upload
:sub_1
    echo okay
    GOTO:eof

:upload
    CHOICE /C:01 /m "Upload build? [0]No, [1]Yes"
        goto up_%ERRORLEVEL%
        
:up_0
    GOTO:eof
:up_1
    upload.cmd
