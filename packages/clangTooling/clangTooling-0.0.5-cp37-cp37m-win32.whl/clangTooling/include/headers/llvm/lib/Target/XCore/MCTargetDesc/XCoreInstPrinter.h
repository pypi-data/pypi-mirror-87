//== XCoreInstPrinter.h - Convert XCore MCInst to assembly syntax -*- C++ -*-=//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
///
/// \file
/// This file contains the declaration of the XCoreInstPrinter class,
/// which is used to print XCore MCInst to a .s file.
///
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_XCORE_MCTARGETDESC_XCOREINSTPRINTER_H
#define LLVM_LIB_TARGET_XCORE_MCTARGETDESC_XCOREINSTPRINTER_H

#include "llvm/ADT/StringRef.h"
#include "llvm/MC/MCInstPrinter.h"

namespace llvm {

class XCoreInstPrinter : public MCInstPrinter {
public:
  XCoreInstPrinter(const MCAsmInfo &MAI, const MCInstrInfo &MII,
                  const MCRegisterInfo &MRI)
    : MCInstPrinter(MAI, MII, MRI) {}

  // Autogenerated by tblgen.
  void printInstruction(const MCInst *MI, uint64_t Address, raw_ostream &O);
  static const char *getRegisterName(unsigned RegNo);

  void printRegName(raw_ostream &OS, unsigned RegNo) const override;
  void printInst(const MCInst *MI, uint64_t Address, StringRef Annot,
                 const MCSubtargetInfo &STI, raw_ostream &O) override;

private:
  void printInlineJT(const MCInst *MI, int opNum, raw_ostream &O);
  void printInlineJT32(const MCInst *MI, int opNum, raw_ostream &O);
  void printOperand(const MCInst *MI, unsigned OpNo, raw_ostream &O);
  void printMemOperand(const MCInst *MI, int opNum, raw_ostream &O);
};

} // end namespace llvm

#endif // LLVM_LIB_TARGET_XCORE_MCTARGETDESC_XCOREINSTPRINTER_H
