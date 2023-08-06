@echo off
rem Copyright 2007-2020 Intel Corporation.
rem 
rem This software and the related documents are Intel copyrighted materials,
rem and your use of them is governed by the express license under which they
rem were provided to you (License). Unless the License provides otherwise,
rem you may not use, modify, copy, publish, distribute, disclose or transmit
rem this software or the related documents without Intel's prior written
rem permission.
rem 
rem This software and the related documents are provided as is, with no
rem express or implied warranties, other than those that are expressly stated
rem in the License.

if not "%SETVARS_CALL%"=="1" goto :MAIN_FUNC
goto :EOF

:MAIN_FUNC
set ROOT_EXCL1=%CONDA_PREFIX%
REM rem PATH is setup automatically by Conda.
set LIB_EXCL1=%CONDA_PREFIX%\Library\bin
set INCLUDE_EXCL1=%CONDA_PREFIX%\Library\include
set PATH_EXCL1=%CONDA_PREFIX%\Library\bin\libfabric\utils
set PATH_EXCL2=%CONDA_PREFIX%\Library\bin\libfabric


if defined I_MPI_ROOT call :FUNC "%I_MPI_ROOT%" "%ROOT_EXCL1%"
set I_MPI_ROOT=%VAR1%

if defined LIB call :FUNC "%LIB%" "%LIB_EXCL1%"
set LIB=%VAR1%

if defined INCLUDE call :FUNC "%INCLUDE%" "%INCLUDE_EXCL1%
set INCLUDE=%VAR1%

if defined Path call :FUNC "%Path%" "%PATH_EXCL1%
set Path=%VAR1%

if defined Path call :FUNC "%Path%" "%PATH_EXCL2%
set Path=%VAR1%

set ROOT_EXCL1=
set LIB_EXCL1=
set INCLUDE_EXCL1=
set PATH_EXCL1=
set PATH_EXCL2=
goto :EOF

:FUNC
set VAR1=%~1
set VAR2=%~2
set TMP_VAR=""

rem Remove all quotes from string
set VAR1=%VAR1:"=%

rem Revome semicolon (;) at the end of line, if it exist.
if "%VAR1:~-1%"==";" set VAR1=%VAR1:~0,-1%

rem Split str on substr by semicolon
for %%i in ("%VAR1:;=";"%") do ( call :sub %%i "%VAR2%" )
set VAR1=%TMP_VAR:?=;%
set VAR1=%VAR1:"=%
exit /b 0

:sub
set _VAR1="%~1"
set _VAR2="%~2"

if NOT %_VAR1% == %_VAR2% (
    if NOT %TMP_VAR% == "" (
      set TMP_VAR=%TMP_VAR%?%_VAR1%
    ) else (
      set TMP_VAR=%_VAR1%
    )
)

exit /b 0
