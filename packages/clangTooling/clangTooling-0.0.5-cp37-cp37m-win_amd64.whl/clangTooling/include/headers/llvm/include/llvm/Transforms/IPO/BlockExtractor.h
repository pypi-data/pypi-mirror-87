//===- BlockExtractor.h - Extracts blocks into their own functions --------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This pass extracts the specified basic blocks from the module into their
// own functions.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_TRANSFORMS_IPO_BLOCKEXTRACTOR_H
#define LLVM_TRANSFORMS_IPO_BLOCKEXTRACTOR_H

#include "llvm/IR/PassManager.h"

namespace llvm {
struct BlockExtractorPass : PassInfoMixin<BlockExtractorPass> {
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM);
};
} // namespace llvm

#endif // LLVM_TRANSFORMS_IPO_BLOCKEXTRACTOR_H
