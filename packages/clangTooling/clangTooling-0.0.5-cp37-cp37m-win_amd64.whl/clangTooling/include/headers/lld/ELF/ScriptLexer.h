//===- ScriptLexer.h --------------------------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef LLD_ELF_SCRIPT_LEXER_H
#define LLD_ELF_SCRIPT_LEXER_H

#include "lld/Common/LLVM.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/Support/MemoryBuffer.h"
#include <utility>
#include <vector>

namespace lld {
namespace elf {

class ScriptLexer {
public:
  explicit ScriptLexer(MemoryBufferRef mb);

  void setError(const Twine &msg);
  void tokenize(MemoryBufferRef mb);
  StringRef skipSpace(StringRef s);
  bool atEOF();
  StringRef next();
  StringRef peek();
  StringRef peek2();
  void skip();
  bool consume(StringRef tok);
  void expect(StringRef expect);
  bool consumeLabel(StringRef tok);
  std::string getCurrentLocation();

  std::vector<MemoryBufferRef> mbs;
  std::vector<StringRef> tokens;
  bool inExpr = false;
  size_t pos = 0;

protected:
  MemoryBufferRef getCurrentMB();

private:
  void maybeSplitExpr();
  StringRef getLine();
  size_t getLineNumber();
  size_t getColumnNumber();
};

} // namespace elf
} // namespace lld

#endif
