#!/bin/sh
#
# Copyright 2003-2020 Intel Corporation.
# 
# This software and the related documents are Intel copyrighted materials, and
# your use of them is governed by the express license under which they were
# provided to you (License). Unless the License provides otherwise, you may
# not use, modify, copy, publish, distribute, disclose or transmit this
# software or the related documents without Intel's prior written permission.
# 
# This software and the related documents are provided as is, with no express
# or implied warranties, other than those that are expressly stated in the
# License.
#
#
# Copyright 2003-2020 Intel Corporation.
# 
# This software and the related documents are Intel copyrighted materials, and
# your use of them is governed by the express license under which they were
# provided to you (License). Unless the License provides otherwise, you may
# not use, modify, copy, publish, distribute, disclose or transmit this
# software or the related documents without Intel's prior written permission.
# 
# This software and the related documents are provided as is, with no express
# or implied warranties, other than those that are expressly stated in the
# License.
#

if [ "${SETVARS_CALL}" != "1" ]
then

    export CLASSPATH=`echo ${CLASSPATH} | sed "s|${CONDA_PREFIX}/lib/mpi.jar:\?||"`
    export LD_LIBRARY_PATH=`echo ${LD_LIBRARY_PATH} | sed "s|${CONDA_PREFIX}/lib/libfabric:\?||"`
    export LD_LIBRARY_PATH=`echo ${LD_LIBRARY_PATH} | sed "s|${CONDA_PREFIX}/lib:\?||"`
    export MANPATH=`echo ${MANPATH} | sed "s|${CONDA_PREFIX}/share/man:\?||"`
    export LIBRARY_PATH=`echo ${LIBRARY_PATH} | sed "s|${CONDA_PREFIX}/lib/libfabric:\?||"`
    export PATH=`echo ${PATH} | sed "s|${CONDA_PREFIX}/bin/libfabric:||"`

    # if fi_info is on the PATH and part of compilers_and_libraries, set I_MPI_ROOT to the root of that location
    FIP=`which fi_info`
    if echo "${FIP}" | grep -q "compilers_and_libraries.*mpi"; then
        export I_MPI_ROOT=`echo ${FIP} | rev| cut -f1 -d' '| rev| sed "s|/intel64/libfabric/bin/fi_info||"`
    # if fi_info is part of oneAPI, set I_MPI_ROOT as root from oneAPI.
    elif echo "${FIP}" | grep -q "inteloneapi/mpi"; then
        export I_MPI_ROOT=`echo ${FIP} | rev| cut -f1 -d' '| rev| sed "s|/libfabric/bin/fi_info||"`
    else
        export I_MPI_ROOT=
    fi

    # only change FI_PROVIDER_PATH if it points to the python prefix
    if echo "${FI_PROVIDER_PATH}" | grep -q "${CONDA_PREFIX}"; then
        # if I_MPI_ROOT is set, set the provider path to MPI's prov dir
        if [[ "${I_MPI_ROOT}" != "" ]]; then
            # if I_MPI_ROOT from oneAPI package
            if echo "${I_MPI_ROOT}" | grep -q "/inteloneapi/"; then
                export FI_PROVIDER_PATH=${I_MPI_ROOT}/libfabric/lib/prov:/usr/lib64/libfabric
            # if I_MPI_ROOT from PSXE package
            else
                export FI_PROVIDER_PATH=${I_MPI_ROOT}/intel64/libfabric/lib/prov:/usr/lib64/libfabric
            fi
        else
            export FI_PROVIDER_PATH=
        fi
    fi
fi
