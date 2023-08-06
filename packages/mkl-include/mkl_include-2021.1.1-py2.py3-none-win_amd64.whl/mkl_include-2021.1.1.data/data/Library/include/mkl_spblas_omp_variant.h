/*******************************************************************************
* Copyright 2020 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

/*
!  Content:
!    Intel(R) Math Kernel Library (Intel(R) MKL) interface for 
!    Sparse BLAS OpenMP compiler offload interface
!******************************************************************************/

#ifndef _MKL_SPBLAS_OMP_VARIANT_H_
#define _MKL_SPBLAS_OMP_VARIANT_H_

#include "mkl_types.h"
#include "mkl_spblas.h"
#include "mkl_omp_variant.h"

#define MKL_SPBLAS_VARIANT_NAME(func) MKL_VARIANT_NAME(sparse, func)

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

    sparse_status_t MKL_SPBLAS_VARIANT_NAME(s_create_csr)( sparse_matrix_t           *A,
                                                         const sparse_index_base_t indexing,
                                                         const MKL_INT             rows,
                                                         const MKL_INT             cols,
                                                               MKL_INT             *rows_start,
                                                               MKL_INT             *rows_end,
                                                               MKL_INT             *col_indx,
                                                               float               *values );

    sparse_status_t MKL_SPBLAS_VARIANT_NAME(d_create_csr)( sparse_matrix_t           *A,
                                                         const sparse_index_base_t indexing,
                                                         const MKL_INT             rows,
                                                         const MKL_INT             cols,
                                                               MKL_INT             *rows_start,
                                                               MKL_INT             *rows_end,
                                                               MKL_INT             *col_indx,
                                                               double              *values );

    sparse_status_t MKL_SPBLAS_VARIANT_NAME(destroy)( sparse_matrix_t  A );

    sparse_status_t MKL_SPBLAS_VARIANT_NAME(s_mv)( const sparse_operation_t  operation,
                                                 const float               alpha,
                                                 const sparse_matrix_t     A,
                                                 const struct matrix_descr descr,
                                                 const float               *x,
                                                 const float               beta,
                                                 float                     *y );

    sparse_status_t MKL_SPBLAS_VARIANT_NAME(d_mv)( const sparse_operation_t  operation,
                                                 const double              alpha,
                                                 const sparse_matrix_t     A,
                                                 const struct matrix_descr descr,
                                                 const double              *x,
                                                 const double              beta,
                                                 double                    *y );

#ifdef __cplusplus
}
#endif /*__cplusplus */

#endif /*_MKL_SPBLAS_OMP_VARIANT_H_ */
