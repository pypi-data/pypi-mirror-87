/*******************************************************************************
* Copyright 2014-2020 Intel Corporation.
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


#ifndef MKL_DAL_DPCPP_HPP
#define MKL_DAL_DPCPP_HPP

#include <CL/sycl.hpp>
#include <cstdint>
#include <complex>

#define DLL_EXPORT

/* add Internal MKL Offset APIs */
#include "mkl_dal_blas_sycl.hpp"

namespace oneapi {
namespace fpk {


enum class transpose : char {
    nontrans = 0,
    trans = 1,
    conjtrans = 3,
    N = 0,
    T = 1,
    C = 3
};

enum class uplo : char {
    upper = 0,
    lower = 1,
    U = 0,
    L = 1
};

enum class diag : char {
    nonunit = 0,
    unit = 1,
    N = 0,
    U = 1
};

enum class side : char {
    left = 0,
    right = 1,
    L = 0,
    R = 1
};

enum class offset : char {
    row = 0,
    column = 1,
    fix = 2,
    R = 0,
    C = 1,
    F = 2
};

enum class job : char {
    novec = 0,
    vec = 1,
    updatevec = 2,
    allvec = 3,
    somevec = 4,
    overwritevec = 5,
    N = 0,
    V = 1,
    U = 2,
    A = 3,
    S = 4,
    O = 5
};

enum class vector : char {
    q = 0,
    p = 1,
    none = 2,
    both = 3,
    Q = 0,
    P = 1,
    N = 2,
    V = 3
};


/* APIs */



class exception : public std::exception {
    std::string msg_;
    public:
        exception(const std::string &domain, const std::string &function, const std::string &info = "") : std::exception() {
            msg_ = std::string("FPK: ") + domain + "/" + function + ((info.length() != 0) ? (": " + info) : "");
        }

        const char* what() const noexcept {
            return msg_.c_str();
        }
};

class unimplemented : public oneapi::fpk::exception {
    public:
        unimplemented(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "function is not implemented "+info) {
        }
};

class invalid_argument : public oneapi::fpk::exception {
    public:
        invalid_argument(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "invalid argument "+info) {
        }
};
class computation_error : public oneapi::fpk::exception {
    public:
        computation_error(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "computation error"+((info.length() != 0) ? (": "+info) : "")) {
        }
};

class batch_error : public oneapi::fpk::exception {
    public:
        batch_error(const std::string &domain, const std::string &function, const std::string &info = "")
            : oneapi::fpk::exception(domain, function, "batch error"+((info.length() != 0) ? (": "+info) : "")) {
        }
};

namespace lapack {

class exception
{
public:
    exception(fpk::exception *_ex, std::int64_t info, std::int64_t detail = 0) : _info(info), _detail(detail), _ex(_ex) {}
    std::int64_t info()   const { return _info; }
    std::int64_t detail() const { return _detail; }
    const char*  what()   const { return _ex->what(); }
private:
    std::int64_t   _info;
    std::int64_t   _detail;
    fpk::exception *_ex;
};

class computation_error : public oneapi::fpk::computation_error, public oneapi::fpk::lapack::exception
{
public:
    computation_error(const std::string &function, const std::string &info, std::int64_t code)
        : oneapi::fpk::computation_error("LAPACK", function, info), oneapi::fpk::lapack::exception(this, code) {}
    using oneapi::fpk::computation_error::what;
};

class batch_error : public oneapi::fpk::batch_error, public oneapi::fpk::lapack::exception
{
public:
    batch_error(const std::string &function, const std::string &info, std::int64_t num_errors, cl::sycl::vector_class<std::int64_t> ids = {}, cl::sycl::vector_class<std::exception_ptr> exceptions = {})
            : oneapi::fpk::batch_error("LAPACK", function, info), oneapi::fpk::lapack::exception(this, num_errors), _ids(ids), _exceptions(exceptions) {}
    using oneapi::fpk::batch_error::what;
    const cl::sycl::vector_class<std::int64_t>& ids() const { return _ids; }
    const cl::sycl::vector_class<std::exception_ptr>& exceptions() const { return _exceptions; }
private:
    cl::sycl::vector_class<std::int64_t> _ids;
    cl::sycl::vector_class<std::exception_ptr> _exceptions;
};

class invalid_argument : public oneapi::fpk::invalid_argument, public oneapi::fpk::lapack::exception
{
public:
    invalid_argument(const std::string &function, const std::string &info, std::int64_t arg_position = 0, std::int64_t detail = 0)
        : oneapi::fpk::invalid_argument("LAPACK", function, info), oneapi::fpk::lapack::exception(this, arg_position, detail) {}
    using oneapi::fpk::invalid_argument::what;
};

class unimplemented : public oneapi::fpk::unimplemented, public oneapi::fpk::lapack::exception
{
public:
    unimplemented(const std::string &function, const std::string &info = "")
        : oneapi::fpk::unimplemented("LAPACK", function, info), oneapi::fpk::lapack::exception(this, -1) {}
    using oneapi::fpk::unimplemented::what;
};

void potrf(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, cl::sycl::buffer<float>  &a, std::int64_t lda, cl::sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void potrf(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, cl::sycl::buffer<double> &a, std::int64_t lda, cl::sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
cl::sycl::event potrf(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, float  *a, std::int64_t lda, float  *scratchpad, std::int64_t scratchpad_size, const cl::sycl::vector_class<cl::sycl::event> &events = {});
cl::sycl::event potrf(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, double *a, std::int64_t lda, double *scratchpad, std::int64_t scratchpad_size, const cl::sycl::vector_class<cl::sycl::event> &events = {});
template <typename data_t, void* = nullptr>
std::int64_t potrf_scratchpad_size(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t lda);

void potrs(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, cl::sycl::buffer<float>  &a, std::int64_t lda, cl::sycl::buffer<float>  &b, std::int64_t ldb, cl::sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void potrs(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, cl::sycl::buffer<double> &a, std::int64_t lda, cl::sycl::buffer<double> &b, std::int64_t ldb, cl::sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
cl::sycl::event potrs(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, float  *a, std::int64_t lda, float  *b, std::int64_t ldb, float  *scratchpad, std::int64_t scratchpad_size, const cl::sycl::vector_class<cl::sycl::event> &events = {});
cl::sycl::event potrs(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, double *a, std::int64_t lda, double *b, std::int64_t ldb, double *scratchpad, std::int64_t scratchpad_size, const cl::sycl::vector_class<cl::sycl::event> &events = {});
template <typename data_t, void* = nullptr>
std::int64_t potrs_scratchpad_size(cl::sycl::queue &queue, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t nrhs, std::int64_t lda, std::int64_t ldb);

void syevd(cl::sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, cl::sycl::buffer<float>  &a, std::int64_t lda, cl::sycl::buffer<float>  &w, cl::sycl::buffer<float>  &scratchpad, std::int64_t scratchpad_size);
void syevd(cl::sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, cl::sycl::buffer<double> &a, std::int64_t lda, cl::sycl::buffer<double> &w, cl::sycl::buffer<double> &scratchpad, std::int64_t scratchpad_size);
template <typename data_t, void* = nullptr>
std::int64_t syevd_scratchpad_size(cl::sycl::queue &queue, oneapi::fpk::job jobz, oneapi::fpk::uplo uplo, std::int64_t n, std::int64_t lda);

} // namespace lapack

namespace blas {
inline namespace column_major {

DLL_EXPORT cl::sycl::event axpy(cl::sycl::queue &queue, std::int64_t n,
    float alpha, const float *x, std::int64_t incx, float *y, std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event axpy(cl::sycl::queue &queue, std::int64_t n,
    double alpha, const double *x, std::int64_t incx, double *y,
    std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event axpy(cl::sycl::queue &queue, std::int64_t n,
    std::complex<float> alpha, const std::complex<float> *x, std::int64_t incx,
    std::complex<float> *y, std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event axpy(cl::sycl::queue &queue, std::int64_t n,
    std::complex<double> alpha, const std::complex<double> *x, std::int64_t incx,
    std::complex<double> *y, std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});


DLL_EXPORT void axpy(cl::sycl::queue &queue, std::int64_t n, float alpha,
    cl::sycl::buffer<float, 1> &x, std::int64_t incx, cl::sycl::buffer<float,
    1> &y, std::int64_t incy);

DLL_EXPORT void axpy(cl::sycl::queue &queue, std::int64_t n, double alpha,
    cl::sycl::buffer<double, 1> &x, std::int64_t incx, cl::sycl::buffer<double,
    1> &y, std::int64_t incy);

DLL_EXPORT void axpy(cl::sycl::queue &queue, std::int64_t n,
    std::complex<float> alpha, cl::sycl::buffer<std::complex<float>, 1> &x,
    std::int64_t incx, cl::sycl::buffer<std::complex<float>, 1> &y,
    std::int64_t incy);

DLL_EXPORT void axpy(cl::sycl::queue &queue, std::int64_t n,
    std::complex<double> alpha, cl::sycl::buffer<std::complex<double>, 1> &x,
    std::int64_t incx, cl::sycl::buffer<std::complex<double>, 1> &y,
    std::int64_t incy);



DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    float alpha, const float *a, std::int64_t lda, const float *b,
    std::int64_t ldb, float beta, float *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    double alpha, const double *a, std::int64_t lda, const double *b,
    std::int64_t ldb, double beta, double *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    std::complex<float> alpha, const std::complex<float> *a, std::int64_t lda,
    const std::complex<float> *b, std::int64_t ldb, std::complex<float> beta,
    std::complex<float> *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    std::complex<double> alpha, const std::complex<double> *a, std::int64_t lda,
    const std::complex<double> *b, std::int64_t ldb, std::complex<double> beta,
    std::complex<double> *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k, half alpha,
    const half *a, std::int64_t lda, const half *b, std::int64_t ldb, half beta,
    half *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    float alpha, const half *a, std::int64_t lda, const half *b,
    std::int64_t ldb, float beta, float *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemm(cl::sycl::queue &queue, transpose transa,
    transpose transb, std::int64_t m, std::int64_t n, std::int64_t k,
    float alpha, const bfloat16 *a, std::int64_t lda, const bfloat16 *b,
    std::int64_t ldb, float beta, float *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});


DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, float alpha,
    cl::sycl::buffer<float, 1> &a, std::int64_t lda, cl::sycl::buffer<float,
    1> &b, std::int64_t ldb, float beta, cl::sycl::buffer<float, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, double alpha,
    cl::sycl::buffer<double, 1> &a, std::int64_t lda, cl::sycl::buffer<double,
    1> &b, std::int64_t ldb, double beta, cl::sycl::buffer<double, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, std::complex<float> alpha,
    cl::sycl::buffer<std::complex<float>, 1> &a, std::int64_t lda,
    cl::sycl::buffer<std::complex<float>, 1> &b, std::int64_t ldb,
    std::complex<float> beta, cl::sycl::buffer<std::complex<float>, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, std::complex<double> alpha,
    cl::sycl::buffer<std::complex<double>, 1> &a, std::int64_t lda,
    cl::sycl::buffer<std::complex<double>, 1> &b, std::int64_t ldb,
    std::complex<double> beta, cl::sycl::buffer<std::complex<double>, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, half alpha,
    cl::sycl::buffer<half, 1> &a, std::int64_t lda, cl::sycl::buffer<half, 1> &b,
    std::int64_t ldb, half beta, cl::sycl::buffer<half, 1> &c, std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, float alpha,
    cl::sycl::buffer<half, 1> &a, std::int64_t lda, cl::sycl::buffer<half, 1> &b,
    std::int64_t ldb, float beta, cl::sycl::buffer<float, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void gemm(cl::sycl::queue &queue, transpose transa, transpose transb,
    std::int64_t m, std::int64_t n, std::int64_t k, float alpha,
    cl::sycl::buffer<bfloat16, 1> &a, std::int64_t lda,
    cl::sycl::buffer<bfloat16, 1> &b, std::int64_t ldb, float beta,
    cl::sycl::buffer<float, 1> &c, std::int64_t ldc);



DLL_EXPORT cl::sycl::event gemv(cl::sycl::queue &queue, transpose trans,
    std::int64_t m, std::int64_t n, float alpha, const float *a,
    std::int64_t lda, const float *x, std::int64_t incx, float beta, float *y,
    std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemv(cl::sycl::queue &queue, transpose trans,
    std::int64_t m, std::int64_t n, double alpha, const double *a,
    std::int64_t lda, const double *x, std::int64_t incx, double beta, double *y,
    std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemv(cl::sycl::queue &queue, transpose trans,
    std::int64_t m, std::int64_t n, std::complex<float> alpha,
    const std::complex<float> *a, std::int64_t lda, const std::complex<float> *x,
    std::int64_t incx, std::complex<float> beta, std::complex<float> *y,
    std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event gemv(cl::sycl::queue &queue, transpose trans,
    std::int64_t m, std::int64_t n, std::complex<double> alpha,
    const std::complex<double> *a, std::int64_t lda,
    const std::complex<double> *x, std::int64_t incx, std::complex<double> beta,
    std::complex<double> *y, std::int64_t incy,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});


DLL_EXPORT void gemv(cl::sycl::queue &queue, transpose trans, std::int64_t m,
    std::int64_t n, float alpha, cl::sycl::buffer<float, 1> &a, std::int64_t lda,
    cl::sycl::buffer<float, 1> &x, std::int64_t incx, float beta,
    cl::sycl::buffer<float, 1> &y, std::int64_t incy);

DLL_EXPORT void gemv(cl::sycl::queue &queue, transpose trans, std::int64_t m,
    std::int64_t n, double alpha, cl::sycl::buffer<double, 1> &a,
    std::int64_t lda, cl::sycl::buffer<double, 1> &x, std::int64_t incx,
    double beta, cl::sycl::buffer<double, 1> &y, std::int64_t incy);

DLL_EXPORT void gemv(cl::sycl::queue &queue, transpose trans, std::int64_t m,
    std::int64_t n, std::complex<float> alpha,
    cl::sycl::buffer<std::complex<float>, 1> &a, std::int64_t lda,
    cl::sycl::buffer<std::complex<float>, 1> &x, std::int64_t incx,
    std::complex<float> beta, cl::sycl::buffer<std::complex<float>, 1> &y,
    std::int64_t incy);

DLL_EXPORT void gemv(cl::sycl::queue &queue, transpose trans, std::int64_t m,
    std::int64_t n, std::complex<double> alpha,
    cl::sycl::buffer<std::complex<double>, 1> &a, std::int64_t lda,
    cl::sycl::buffer<std::complex<double>, 1> &x, std::int64_t incx,
    std::complex<double> beta, cl::sycl::buffer<std::complex<double>, 1> &y,
    std::int64_t incy);



DLL_EXPORT cl::sycl::event syrk(cl::sycl::queue &queue, uplo upper_lower,
    transpose trans, std::int64_t n, std::int64_t k, float alpha, const float *a,
    std::int64_t lda, float beta, float *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event syrk(cl::sycl::queue &queue, uplo upper_lower,
    transpose trans, std::int64_t n, std::int64_t k, double alpha,
    const double *a, std::int64_t lda, double beta, double *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event syrk(cl::sycl::queue &queue, uplo upper_lower,
    transpose trans, std::int64_t n, std::int64_t k, std::complex<float> alpha,
    const std::complex<float> *a, std::int64_t lda, std::complex<float> beta,
    std::complex<float> *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});

DLL_EXPORT cl::sycl::event syrk(cl::sycl::queue &queue, uplo upper_lower,
    transpose trans, std::int64_t n, std::int64_t k, std::complex<double> alpha,
    const std::complex<double> *a, std::int64_t lda, std::complex<double> beta,
    std::complex<double> *c, std::int64_t ldc,
    const cl::sycl::vector_class<cl::sycl::event> &dependencies = {});


DLL_EXPORT void syrk(cl::sycl::queue &queue, uplo upper_lower, transpose trans,
    std::int64_t n, std::int64_t k, float alpha, cl::sycl::buffer<float, 1> &a,
    std::int64_t lda, float beta, cl::sycl::buffer<float, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void syrk(cl::sycl::queue &queue, uplo upper_lower, transpose trans,
    std::int64_t n, std::int64_t k, double alpha, cl::sycl::buffer<double, 1> &a,
    std::int64_t lda, double beta, cl::sycl::buffer<double, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void syrk(cl::sycl::queue &queue, uplo upper_lower, transpose trans,
    std::int64_t n, std::int64_t k, std::complex<float> alpha,
    cl::sycl::buffer<std::complex<float>, 1> &a, std::int64_t lda,
    std::complex<float> beta, cl::sycl::buffer<std::complex<float>, 1> &c,
    std::int64_t ldc);

DLL_EXPORT void syrk(cl::sycl::queue &queue, uplo upper_lower, transpose trans,
    std::int64_t n, std::int64_t k, std::complex<double> alpha,
    cl::sycl::buffer<std::complex<double>, 1> &a, std::int64_t lda,
    std::complex<double> beta, cl::sycl::buffer<std::complex<double>, 1> &c,
    std::int64_t ldc);


 } // namespace column_major
 } // namespace blas







/* end APIs */

} /* namespace fpk */
} /* namespace oneapi */
#endif /*MKL_DAL_DPCPP_HPP*/
