/*******************************************************************************
* Copyright 2019-2020 Intel Corporation.
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

// Internal BLAS entrypoints.
// 
// Unlike the external API, these interfaces support offsets into input buffers.

#ifndef FPK_BLAS_SYCL_HPP
#define FPK_BLAS_SYCL_HPP

#include <CL/sycl.hpp>
#include <cstdint>

extern "C" {

typedef enum {
    MKL_NOTRANS = 111,
    MKL_TRANS = 112,
    MKL_CONJTRANS = 113
} MKL_TRANSPOSE;

typedef enum {
    MKL_UPPER = 121,
    MKL_LOWER = 122
} MKL_UPLO;

typedef enum {
    MKL_ROW_MAJOR = 101,
    MKL_COL_MAJOR = 102
} MKL_LAYOUT;

}

namespace oneapi {
namespace fpk {

struct bfloat16 {
    uint16_t bits;
};

namespace gpu {
 
cl::sycl::event sgemm_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_TRANSPOSE transa, MKL_TRANSPOSE transb, int64_t m, int64_t n, int64_t k, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, cl::sycl::buffer<float,1> *b, int64_t ldb, float beta, cl::sycl::buffer<float,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_b = 0, int64_t offset_c = 0);

cl::sycl::event dgemm_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_TRANSPOSE transa, MKL_TRANSPOSE transb, int64_t m, int64_t n, int64_t k, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, cl::sycl::buffer<double,1> *b, int64_t ldb, double beta, cl::sycl::buffer<double,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_b = 0, int64_t offset_c = 0);

cl::sycl::event ssyrk_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_UPLO upper_lower, MKL_TRANSPOSE trans, int64_t n, int64_t k, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, float beta, cl::sycl::buffer<float,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_c = 0);

cl::sycl::event dsyrk_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_UPLO upper_lower, MKL_TRANSPOSE trans, int64_t n, int64_t k, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, double beta, cl::sycl::buffer<double,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_c = 0);

cl::sycl::event sgemv_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_TRANSPOSE trans, int64_t m, int64_t n, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, cl::sycl::buffer<float,1> *x, int64_t incx, float beta, cl::sycl::buffer<float,1> *y, int64_t incy, int64_t offset_a = 0, int64_t offset_x = 0, int64_t offset_y = 0);

cl::sycl::event dgemv_sycl(cl::sycl::queue *queue, MKL_LAYOUT layout, MKL_TRANSPOSE trans, int64_t m, int64_t n, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, cl::sycl::buffer<double,1> *x, int64_t incx, double beta, cl::sycl::buffer<double,1> *y, int64_t incy, int64_t offset_a = 0, int64_t offset_x = 0, int64_t offset_y = 0);


static inline void sgemm_sycl(cl::sycl::queue *queue, MKL_TRANSPOSE transa, MKL_TRANSPOSE transb, int64_t m, int64_t n, int64_t k, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, cl::sycl::buffer<float,1> *b, int64_t ldb, float beta, cl::sycl::buffer<float,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_b = 0, int64_t offset_c = 0)
{
    sgemm_sycl(queue, MKL_COL_MAJOR, transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc, offset_a, offset_b, offset_c);
}

static inline void dgemm_sycl(cl::sycl::queue *queue, MKL_TRANSPOSE transa, MKL_TRANSPOSE transb, int64_t m, int64_t n, int64_t k, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, cl::sycl::buffer<double,1> *b, int64_t ldb, double beta, cl::sycl::buffer<double,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_b = 0, int64_t offset_c = 0)
{
    dgemm_sycl(queue, MKL_COL_MAJOR, transa, transb, m, n, k, alpha, a, lda, b, ldb, beta, c, ldc, offset_a, offset_b, offset_c);
}

static inline void ssyrk_sycl(cl::sycl::queue *queue, MKL_UPLO upper_lower, MKL_TRANSPOSE trans, int64_t n, int64_t k, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, float beta, cl::sycl::buffer<float,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_c = 0)
{
    ssyrk_sycl(queue, MKL_COL_MAJOR, upper_lower, trans, n, k, alpha, a, lda, beta, c, ldc, offset_a, offset_c);
}

static inline void dsyrk_sycl(cl::sycl::queue *queue, MKL_UPLO upper_lower, MKL_TRANSPOSE trans, int64_t n, int64_t k, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, double beta, cl::sycl::buffer<double,1> *c, int64_t ldc, int64_t offset_a = 0, int64_t offset_c = 0)
{
    dsyrk_sycl(queue, MKL_COL_MAJOR, upper_lower, trans, n, k, alpha, a, lda, beta, c, ldc, offset_a, offset_c);
}

static inline void sgemv_sycl(cl::sycl::queue *queue, MKL_TRANSPOSE trans, int64_t m, int64_t n, float alpha, cl::sycl::buffer<float,1> *a, int64_t lda, cl::sycl::buffer<float,1> *x, int64_t incx, float beta, cl::sycl::buffer<float,1> *y, int64_t incy, int64_t offset_a = 0, int64_t offset_x = 0, int64_t offset_y = 0)
{
    sgemv_sycl(queue, MKL_COL_MAJOR, trans, m, n, alpha, a, lda, x, incx, beta, y, incy, offset_a, offset_x, offset_y);
}

static inline void dgemv_sycl(cl::sycl::queue *queue, MKL_TRANSPOSE trans, int64_t m, int64_t n, double alpha, cl::sycl::buffer<double,1> *a, int64_t lda, cl::sycl::buffer<double,1> *x, int64_t incx, double beta, cl::sycl::buffer<double,1> *y, int64_t incy, int64_t offset_a = 0, int64_t offset_x = 0, int64_t offset_y = 0)
{
    dgemv_sycl(queue, MKL_COL_MAJOR, trans, m, n, alpha, a, lda, x, incx, beta, y, incy, offset_a, offset_x, offset_y);
}

} // namespace gpu
} // namespace fpk
} // namespace oneapi

#endif /* header guard */
