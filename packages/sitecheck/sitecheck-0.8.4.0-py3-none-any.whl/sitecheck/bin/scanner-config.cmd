@echo off

:init
 setlocal DisableDelayedExpansion
 set cmdInvoke=1
 set winSysFolder=System32
 set "batchPath=%~0"
 for %%k in (%0) do set batchName=%%~nk
 set "vbsGetPrivileges=%temp%\OEgetPriv_%batchName%.vbs"
 setlocal EnableDelayedExpansion

:checkPrivileges
  NET FILE 1>NUL 2>NUL
  if '%errorlevel%' == '0' ( goto gotPrivileges ) else ( goto getPrivileges )

:getPrivileges
  if '%1'=='ELEV' (echo ELEV & shift /1 & goto gotPrivileges)
  ECHO.

  ECHO Set UAC = CreateObject^("Shell.Application"^) > "%vbsGetPrivileges%"
  ECHO args = "ELEV " >> "%vbsGetPrivileges%"
  ECHO For Each strArg in WScript.Arguments >> "%vbsGetPrivileges%"
  ECHO args = args ^& strArg ^& " "  >> "%vbsGetPrivileges%"
  ECHO Next >> "%vbsGetPrivileges%"

  if '%cmdInvoke%'=='1' goto InvokeCmd

  ECHO UAC.ShellExecute "!batchPath!", args, "", "runas", 1 >> "%vbsGetPrivileges%"
  goto ExecElevation

:InvokeCmd
  ECHO args = "/c """ + "!batchPath!" + """ " + args >> "%vbsGetPrivileges%"
  ECHO UAC.ShellExecute "%SystemRoot%\%winSysFolder%\cmd.exe", args, "", "runas", 1 >> "%vbsGetPrivileges%"

:ExecElevation
 "%SystemRoot%\%winSysFolder%\WScript.exe" "%vbsGetPrivileges%" %*
 exit /B

:gotPrivileges
 setlocal & cd /d %~dp0
 if '%1'=='ELEV' (del "%vbsGetPrivileges%" 1>nul 2>nul  &  shift /1)

 ::START
 ::::::::::::::::::::::::::::
call %0

GOTO:login_1

:dev

CHOICE /C:01 /m "Login set? [0]set 1, [1]set 2"    
        goto login_%ERRORLEVEL%
 REM :login_0
set /P "SCANNER_AMPUSER=Enter your Amp user: "
set /P "SCANNER_AMPPASS=Enter your Amp pass: "

:login_1
set /P "SCANNER_AMPUSER=Enter your Amp user: "
set /P "SCANNER_AMPPASS=Enter your Amp pass: "


set /P "SCANNER_QVUSER=Enter your QV username: "
set /P "SCANNER_QVPASS=Enter your QV pass: "

set /P "SCANNER_IP=Enter your mqtt host: "
set /P "SCANNER_PORT=Enter your mqtt port: "

setx SCANNER_AMPUSER %SCANNER_AMPUSER%
setx SCANNER_QVUSER %SCANNER_QVUSER%
setx SCANNER_AMPPASS %SCANNER_AMPPASS%
setx SCANNER_QVPASS %SCANNER_QVPASS%
setx SCANNER_IP %SCANNER_IP%
setx SCANNER_PORT %SCANNER_PORT%


echo %SCANNER_AMPUSER% set.
echo %SCANNER_AMPPASS% set.
echo %SCANNER_QVUSER% set.
echo %SCANNER_QVPASS% set.
echo %SCANNER_IP% set.
echo %SCANNER_PORT% set.

REM important to exit out of the shell so the environment refreshes
exit
