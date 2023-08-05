//===- ARMLegalizerInfo ------------------------------------------*- C++ -*-==//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
/// \file
/// This file declares the targeting of the Machinelegalizer class for ARM.
/// \todo This should be generated by TableGen.
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_ARM_ARMMACHINELEGALIZER_H
#define LLVM_LIB_TARGET_ARM_ARMMACHINELEGALIZER_H

#include "llvm/ADT/IndexedMap.h"
#include "llvm/CodeGen/GlobalISel/GISelChangeObserver.h"
#include "llvm/CodeGen/GlobalISel/LegalizerInfo.h"
#include "llvm/CodeGen/RuntimeLibcalls.h"
#include "llvm/IR/Instructions.h"

namespace llvm {

class ARMSubtarget;

/// This class provides the information for the target register banks.
class ARMLegalizerInfo : public LegalizerInfo {
public:
  ARMLegalizerInfo(const ARMSubtarget &ST);

  bool legalizeCustom(LegalizerHelper &Helper, MachineInstr &MI) const override;

private:
  void setFCmpLibcallsGNU();
  void setFCmpLibcallsAEABI();

  struct FCmpLibcallInfo {
    // Which libcall this is.
    RTLIB::Libcall LibcallID;

    // The predicate to be used when comparing the value returned by the
    // function with a relevant constant (currently hard-coded to zero). This is
    // necessary because often the libcall will return e.g. a value greater than
    // 0 to represent 'true' and anything negative to represent 'false', or
    // maybe 0 to represent 'true' and non-zero for 'false'. If no comparison is
    // needed, this should be CmpInst::BAD_ICMP_PREDICATE.
    CmpInst::Predicate Predicate;
  };
  using FCmpLibcallsList = SmallVector<FCmpLibcallInfo, 2>;

  // Map from each FCmp predicate to the corresponding libcall infos. A FCmp
  // instruction may be lowered to one or two libcalls, which is why we need a
  // list. If two libcalls are needed, their results will be OR'ed.
  using FCmpLibcallsMapTy = IndexedMap<FCmpLibcallsList>;

  FCmpLibcallsMapTy FCmp32Libcalls;
  FCmpLibcallsMapTy FCmp64Libcalls;

  // Get the libcall(s) corresponding to \p Predicate for operands of \p Size
  // bits.
  FCmpLibcallsList getFCmpLibcalls(CmpInst::Predicate, unsigned Size) const;
};
} // End llvm namespace.
#endif
