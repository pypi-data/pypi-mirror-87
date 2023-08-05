//= NVPTXInstPrinter.h - Convert NVPTX MCInst to assembly syntax --*- C++ -*-=//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This class prints an NVPTX MCInst to .ptx file syntax.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_LIB_TARGET_NVPTX_MCTARGETDESC_NVPTXINSTPRINTER_H
#define LLVM_LIB_TARGET_NVPTX_MCTARGETDESC_NVPTXINSTPRINTER_H

#include "llvm/MC/MCInstPrinter.h"

namespace llvm {

class MCSubtargetInfo;

class NVPTXInstPrinter : public MCInstPrinter {
public:
  NVPTXInstPrinter(const MCAsmInfo &MAI, const MCInstrInfo &MII,
                   const MCRegisterInfo &MRI);

  void printRegName(raw_ostream &OS, unsigned RegNo) const override;
  void printInst(const MCInst *MI, uint64_t Address, StringRef Annot,
                 const MCSubtargetInfo &STI, raw_ostream &OS) override;

  // Autogenerated by tblgen.
  std::pair<const char *, uint64_t> getMnemonic(const MCInst *MI) override;
  void printInstruction(const MCInst *MI, uint64_t Address, raw_ostream &O);
  static const char *getRegisterName(unsigned RegNo);
  // End

  void printOperand(const MCInst *MI, unsigned OpNo, raw_ostream &O);
  void printCvtMode(const MCInst *MI, int OpNum, raw_ostream &O,
                    const char *Modifier = nullptr);
  void printCmpMode(const MCInst *MI, int OpNum, raw_ostream &O,
                    const char *Modifier = nullptr);
  void printLdStCode(const MCInst *MI, int OpNum,
                     raw_ostream &O, const char *Modifier = nullptr);
  void printMmaCode(const MCInst *MI, int OpNum, raw_ostream &O,
                    const char *Modifier = nullptr);
  void printMemOperand(const MCInst *MI, int OpNum,
                       raw_ostream &O, const char *Modifier = nullptr);
  void printProtoIdent(const MCInst *MI, int OpNum,
                       raw_ostream &O, const char *Modifier = nullptr);
};

}

#endif
