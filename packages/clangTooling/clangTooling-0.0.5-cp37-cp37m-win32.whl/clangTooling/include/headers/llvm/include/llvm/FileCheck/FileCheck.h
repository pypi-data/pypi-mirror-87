//==-- llvm/FileCheck/FileCheck.h --------------------------------*- C++ -*-==//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
/// \file This file has some utilities to use FileCheck as an API
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_FILECHECK_FILECHECK_H
#define LLVM_FILECHECK_FILECHECK_H

#include "llvm/ADT/StringRef.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/Regex.h"
#include "llvm/Support/SourceMgr.h"
#include <string>
#include <vector>

namespace llvm {

/// Contains info about various FileCheck options.
struct FileCheckRequest {
  std::vector<StringRef> CheckPrefixes;
  std::vector<StringRef> CommentPrefixes;
  bool NoCanonicalizeWhiteSpace = false;
  std::vector<StringRef> ImplicitCheckNot;
  std::vector<StringRef> GlobalDefines;
  bool AllowEmptyInput = false;
  bool AllowUnusedPrefixes = false;
  bool MatchFullLines = false;
  bool IgnoreCase = false;
  bool IsDefaultCheckPrefix = false;
  bool EnableVarScope = false;
  bool AllowDeprecatedDagOverlap = false;
  bool Verbose = false;
  bool VerboseVerbose = false;
};

namespace Check {

enum FileCheckKind {
  CheckNone = 0,
  CheckPlain,
  CheckNext,
  CheckSame,
  CheckNot,
  CheckDAG,
  CheckLabel,
  CheckEmpty,
  CheckComment,

  /// Indicates the pattern only matches the end of file. This is used for
  /// trailing CHECK-NOTs.
  CheckEOF,

  /// Marks when parsing found a -NOT check combined with another CHECK suffix.
  CheckBadNot,

  /// Marks when parsing found a -COUNT directive with invalid count value.
  CheckBadCount
};

class FileCheckType {
  FileCheckKind Kind;
  int Count; ///< optional Count for some checks

public:
  FileCheckType(FileCheckKind Kind = CheckNone) : Kind(Kind), Count(1) {}
  FileCheckType(const FileCheckType &) = default;
  FileCheckType &operator=(const FileCheckType &) = default;

  operator FileCheckKind() const { return Kind; }

  int getCount() const { return Count; }
  FileCheckType &setCount(int C);

  // \returns a description of \p Prefix.
  std::string getDescription(StringRef Prefix) const;
};
} // namespace Check

/// Summary of a FileCheck diagnostic.
struct FileCheckDiag {
  /// What is the FileCheck directive for this diagnostic?
  Check::FileCheckType CheckTy;
  /// Where is the FileCheck directive for this diagnostic?
  SMLoc CheckLoc;
  /// What type of match result does this diagnostic describe?
  ///
  /// A directive's supplied pattern is said to be either expected or excluded
  /// depending on whether the pattern must have or must not have a match in
  /// order for the directive to succeed.  For example, a CHECK directive's
  /// pattern is expected, and a CHECK-NOT directive's pattern is excluded.
  /// All match result types whose names end with "Excluded" are for excluded
  /// patterns, and all others are for expected patterns.
  ///
  /// There might be more than one match result for a single pattern.  For
  /// example, there might be several discarded matches
  /// (MatchFoundButDiscarded) before either a good match
  /// (MatchFoundAndExpected) or a failure to match (MatchNoneButExpected),
  /// and there might be a fuzzy match (MatchFuzzy) after the latter.
  enum MatchType {
    /// Indicates a good match for an expected pattern.
    MatchFoundAndExpected,
    /// Indicates a match for an excluded pattern.
    MatchFoundButExcluded,
    /// Indicates a match for an expected pattern, but the match is on the
    /// wrong line.
    MatchFoundButWrongLine,
    /// Indicates a discarded match for an expected pattern.
    MatchFoundButDiscarded,
    /// Indicates no match for an excluded pattern.
    MatchNoneAndExcluded,
    /// Indicates no match for an expected pattern, but this might follow good
    /// matches when multiple matches are expected for the pattern, or it might
    /// follow discarded matches for the pattern.
    MatchNoneButExpected,
    /// Indicates a fuzzy match that serves as a suggestion for the next
    /// intended match for an expected pattern with too few or no good matches.
    MatchFuzzy,
  } MatchTy;
  /// The search range if MatchTy is MatchNoneAndExcluded or
  /// MatchNoneButExpected, or the match range otherwise.
  unsigned InputStartLine;
  unsigned InputStartCol;
  unsigned InputEndLine;
  unsigned InputEndCol;
  /// A note to replace the one normally indicated by MatchTy, or the empty
  /// string if none.
  std::string Note;
  FileCheckDiag(const SourceMgr &SM, const Check::FileCheckType &CheckTy,
                SMLoc CheckLoc, MatchType MatchTy, SMRange InputRange,
                StringRef Note = "");
};

class FileCheckPatternContext;
struct FileCheckString;

/// FileCheck class takes the request and exposes various methods that
/// use information from the request.
class FileCheck {
  FileCheckRequest Req;
  std::unique_ptr<FileCheckPatternContext> PatternContext;
  // C++17 TODO: make this a plain std::vector.
  std::unique_ptr<std::vector<FileCheckString>> CheckStrings;

public:
  explicit FileCheck(FileCheckRequest Req);
  ~FileCheck();

  // Combines the check prefixes into a single regex so that we can efficiently
  // scan for any of the set.
  //
  // The semantics are that the longest-match wins which matches our regex
  // library.
  Regex buildCheckPrefixRegex();

  /// Reads the check file from \p Buffer and records the expected strings it
  /// contains. Errors are reported against \p SM.
  ///
  /// Only expected strings whose prefix is one of those listed in \p PrefixRE
  /// are recorded. \returns true in case of an error, false otherwise.
  ///
  /// If \p ImpPatBufferIDRange, then the range (inclusive start, exclusive end)
  /// of IDs for source buffers added to \p SM for implicit patterns are
  /// recorded in it.  The range is empty if there are none.
  bool
  readCheckFile(SourceMgr &SM, StringRef Buffer, Regex &PrefixRE,
                std::pair<unsigned, unsigned> *ImpPatBufferIDRange = nullptr);

  bool ValidateCheckPrefixes();

  /// Canonicalizes whitespaces in the file. Line endings are replaced with
  /// UNIX-style '\n'.
  StringRef CanonicalizeFile(MemoryBuffer &MB,
                             SmallVectorImpl<char> &OutputBuffer);

  /// Checks the input to FileCheck provided in the \p Buffer against the
  /// expected strings read from the check file and record diagnostics emitted
  /// in \p Diags. Errors are recorded against \p SM.
  ///
  /// \returns false if the input fails to satisfy the checks.
  bool checkInput(SourceMgr &SM, StringRef Buffer,
                  std::vector<FileCheckDiag> *Diags = nullptr);
};

} // namespace llvm

#endif
