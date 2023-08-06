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
Rem Intel(R) MPI Library Build Environment

if not "%SETVARS_CALL%"=="1" goto :MAIN_FUNC
goto :EOF

:MAIN_FUNC
set I_MPI_ROOT=%CONDA_PREFIX%;%I_MPI_ROOT%
Rem PATH is setup by Conda automatically.
set LIB=%CONDA_PREFIX%\Library\bin;%LIB%
set INCLUDE=%CONDA_PREFIX%\Library\include;%INCLUDE%

if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="0" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="no" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="off" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="disable" goto :EOF
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="1" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="yes" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="on" goto SET_LIBFABRIC_PATH
if /i "%I_MPI_OFI_LIBRARY_INTERNAL%"=="enable" goto SET_LIBFABRIC_PATH

where libfabric.dll >nul 2>&1
if not "%errorlevel%"=="0" goto SET_LIBFABRIC_PATH

"%CONDA_PREFIX%\Library\bin\libfabric\utils\fi_info.exe" --version >nul 2>&1
if not "%errorlevel%"=="0" goto SET_LIBFABRIC_PATH

where fi_info.exe >nul 2>&1
if not "%errorlevel%"=="0" set PATH=%CONDA_PREFIX%\Library\bin\libfabric\utils;%PATH%
exit /b 0


:SET_LIBFABRIC_PATH
set PATH=%CONDA_PREFIX%\Library\bin\libfabric\utils;%CONDA_PREFIX%\Library\bin\libfabric;%PATH%
exit /b 0
