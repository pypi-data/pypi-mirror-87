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

rem ----------------------------------------------------------------------------
rem mpicxx.bat
rem Simple script to compile and/or link MPI programs by Intel C++ Compiler.
rem This script sets some variable and the general script.
rem ----------------------------------------------------------------------------

rem We need to use CXX lib additionally 
set need_cxx_lib=yes

rem Invoke C/C++ version of driver
call mpicc.bat %*

