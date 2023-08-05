//===- PPCTargetStreamer.h - PPC Target Streamer ----------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_POWERPC_PPCTARGETSTREAMER_H
#define LLVM_LIB_TARGET_POWERPC_PPCTARGETSTREAMER_H

#include "llvm/ADT/StringRef.h"
#include "llvm/MC/MCStreamer.h"

namespace llvm {

class MCExpr;
class MCSymbol;
class MCSymbolELF;

class PPCTargetStreamer : public MCTargetStreamer {
public:
  PPCTargetStreamer(MCStreamer &S);
  ~PPCTargetStreamer() override;

  virtual void emitTCEntry(const MCSymbol &S) = 0;
  virtual void emitMachine(StringRef CPU) = 0;
  virtual void emitAbiVersion(int AbiVersion) = 0;
  virtual void emitLocalEntry(MCSymbolELF *S, const MCExpr *LocalOffset) = 0;
};

} // end namespace llvm

#endif // LLVM_LIB_TARGET_POWERPC_PPCTARGETSTREAMER_H
