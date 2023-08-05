// CodeGen/RuntimeLibcallSignatures.h - R.T. Lib. Call Signatures -*- C++ -*--//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
///
/// \file
/// This file provides signature information for runtime libcalls.
///
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_WEBASSEMBLY_RUNTIME_LIBCALL_SIGNATURES_H
#define LLVM_LIB_TARGET_WEBASSEMBLY_RUNTIME_LIBCALL_SIGNATURES_H

#include "MCTargetDesc/WebAssemblyMCTargetDesc.h"
#include "llvm/ADT/SmallVector.h"
#include "llvm/CodeGen/RuntimeLibcalls.h"

namespace llvm {

class WebAssemblySubtarget;

extern void getLibcallSignature(const WebAssemblySubtarget &Subtarget,
                                RTLIB::Libcall LC,
                                SmallVectorImpl<wasm::ValType> &Rets,
                                SmallVectorImpl<wasm::ValType> &Params);

extern void getLibcallSignature(const WebAssemblySubtarget &Subtarget,
                                const char *Name,
                                SmallVectorImpl<wasm::ValType> &Rets,
                                SmallVectorImpl<wasm::ValType> &Params);

} // end namespace llvm

#endif
