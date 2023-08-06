/* ************************************************************************
 * Copyright (c) 2018-2020 Advanced Micro Devices, Inc.
 *
 * ************************************************************************ */

#ifndef ROCALUTION_VERSION_HPP_
#define ROCALUTION_VERSION_HPP_

// clang-format off
#define __ROCALUTION_VER_MAJOR     1
#define __ROCALUTION_VER_MINOR     10
#define __ROCALUTION_VER_PATCH     1
#define __ROCALUTION_VER_TWEAK     538-rocm-rel-3.10-27-45e39fb
// clang-format on

// BETA or ALPHA
#define __ROCALUTION_VER_PRE ""
//#define __ROCALUTION_VER_PRE "ALPHA"
//#define __ROCALUTION_VER_PRE "BETA"

#define __ROCALUTION_VER \
    10000 * __ROCALUTION_VER_MAJOR + 100 * __ROCALUTION_VER_MINOR + __ROCALUTION_VER_PATCH

#endif // ROCALUTION_VERSION_HPP_
