//===- AnalysisDeclContext.h - Context for path sensitivity -----*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
/// \file
/// This file defines AnalysisDeclContext, a class that manages the analysis
/// context data for context sensitive and path sensitive analysis.
/// It also defines the helper classes to model entering, leaving or inlining
/// function calls.
//
//===----------------------------------------------------------------------===//

#ifndef LLVM_CLANG_ANALYSIS_ANALYSISDECLCONTEXT_H
#define LLVM_CLANG_ANALYSIS_ANALYSISDECLCONTEXT_H

#include "clang/AST/DeclBase.h"
#include "clang/Analysis/BodyFarm.h"
#include "clang/Analysis/CFG.h"
#include "clang/Analysis/CodeInjector.h"
#include "clang/Basic/LLVM.h"
#include "llvm/ADT/DenseMap.h"
#include "llvm/ADT/FoldingSet.h"
#include "llvm/ADT/StringRef.h"
#include "llvm/ADT/iterator_range.h"
#include "llvm/Support/Allocator.h"
#include <functional>
#include <memory>

namespace clang {

class AnalysisDeclContextManager;
class ASTContext;
class BlockDecl;
class BlockInvocationContext;
class CFGReverseBlockReachabilityAnalysis;
class CFGStmtMap;
class ImplicitParamDecl;
class LocationContext;
class LocationContextManager;
class ParentMap;
class StackFrameContext;
class Stmt;
class VarDecl;

/// The base class of a hierarchy of objects representing analyses tied
/// to AnalysisDeclContext.
class ManagedAnalysis {
protected:
  ManagedAnalysis() = default;

public:
  virtual ~ManagedAnalysis();

  // Subclasses need to implement:
  //
  //  static const void *getTag();
  //
  // Which returns a fixed pointer address to distinguish classes of
  // analysis objects.  They also need to implement:
  //
  //  static [Derived*] create(AnalysisDeclContext &Ctx);
  //
  // which creates the analysis object given an AnalysisDeclContext.
};

/// AnalysisDeclContext contains the context data for the function, method
/// or block under analysis.
class AnalysisDeclContext {
  // Backpoint to the AnalysisManager object that created this
  // AnalysisDeclContext. This may be null.
  AnalysisDeclContextManager *ADCMgr;

  const Decl *const D;

  std::unique_ptr<CFG> cfg, completeCFG;
  std::unique_ptr<CFGStmtMap> cfgStmtMap;

  CFG::BuildOptions cfgBuildOptions;
  CFG::BuildOptions::ForcedBlkExprs *forcedBlkExprs = nullptr;

  bool builtCFG = false;
  bool builtCompleteCFG = false;
  std::unique_ptr<ParentMap> PM;
  std::unique_ptr<CFGReverseBlockReachabilityAnalysis> CFA;

  llvm::BumpPtrAllocator A;

  llvm::DenseMap<const BlockDecl *, void *> *ReferencedBlockVars = nullptr;

  void *ManagedAnalyses = nullptr;

public:
  AnalysisDeclContext(AnalysisDeclContextManager *Mgr, const Decl *D);

  AnalysisDeclContext(AnalysisDeclContextManager *Mgr, const Decl *D,
                      const CFG::BuildOptions &BuildOptions);

  ~AnalysisDeclContext();

  ASTContext &getASTContext() const { return D->getASTContext(); }

  const Decl *getDecl() const { return D; }

  AnalysisDeclContextManager *getManager() const { return ADCMgr; }

  CFG::BuildOptions &getCFGBuildOptions() { return cfgBuildOptions; }

  const CFG::BuildOptions &getCFGBuildOptions() const {
    return cfgBuildOptions;
  }

  /// \returns Whether we are adding exception handling edges from CallExprs.
  /// If this is false, then try/catch statements and blocks reachable from them
  /// can appear to be dead in the CFG, analysis passes must cope with that.
  bool getAddEHEdges() const { return cfgBuildOptions.AddEHEdges; }
  bool getUseUnoptimizedCFG() const {
    return !cfgBuildOptions.PruneTriviallyFalseEdges;
  }
  bool getAddImplicitDtors() const { return cfgBuildOptions.AddImplicitDtors; }
  bool getAddInitializers() const { return cfgBuildOptions.AddInitializers; }

  void registerForcedBlockExpression(const Stmt *stmt);
  const CFGBlock *getBlockForRegisteredExpression(const Stmt *stmt);

  /// \returns The body of the stored Decl \c D.
  Stmt *getBody() const;

  /// \copydoc AnalysisDeclContext::getBody()
  /// \param[out] IsAutosynthesized Specifies if the body is auto-generated
  ///             by the BodyFarm.
  Stmt *getBody(bool &IsAutosynthesized) const;

  /// \returns Whether the body of the Decl \c D is generated by the BodyFarm.
  ///
  /// \note The lookup is not free. We are going to call getBody behind
  /// the scenes.
  /// \sa getBody
  bool isBodyAutosynthesized() const;

  /// \returns Whether the body of the Decl \c D is generated by the BodyFarm
  /// from a model file.
  ///
  /// \note The lookup is not free. We are going to call getBody behind
  /// the scenes.
  /// \sa getBody
  bool isBodyAutosynthesizedFromModelFile() const;

  CFG *getCFG();

  CFGStmtMap *getCFGStmtMap();

  CFGReverseBlockReachabilityAnalysis *getCFGReachablityAnalysis();

  /// \returns A version of the CFG without any edges pruned.
  CFG *getUnoptimizedCFG();

  void dumpCFG(bool ShowColors);

  /// \returns Whether we have built a CFG for this analysis context.
  ///
  /// \note This doesn't correspond to whether or not a valid CFG exists, it
  /// corresponds to whether we *attempted* to build one.
  bool isCFGBuilt() const { return builtCFG; }

  ParentMap &getParentMap();

  using referenced_decls_iterator = const VarDecl *const *;

  llvm::iterator_range<referenced_decls_iterator>
  getReferencedBlockVars(const BlockDecl *BD);

  /// \returns The ImplicitParamDecl associated with \c self if this
  /// AnalysisDeclContext wraps an ObjCMethodDecl or nullptr otherwise.
  const ImplicitParamDecl *getSelfDecl() const;

  /// \copydoc LocationContextManager::getStackFrame()
  const StackFrameContext *getStackFrame(LocationContext const *ParentLC,
                                         const Stmt *S, const CFGBlock *Blk,
                                         unsigned BlockCount, unsigned Index);

  /// \copydoc LocationContextManager::getBlockInvocationContext()
  const BlockInvocationContext *
  getBlockInvocationContext(const LocationContext *ParentLC,
                            const BlockDecl *BD, const void *Data);

  /// \returns The specified analysis object, lazily running the analysis if
  /// necessary or nullptr if the analysis could not run.
  template <typename T> T *getAnalysis() {
    const void *tag = T::getTag();
    std::unique_ptr<ManagedAnalysis> &data = getAnalysisImpl(tag);
    if (!data)
      data = T::create(*this);
    return static_cast<T *>(data.get());
  }

  /// \returns Whether the root namespace of \p D is the \c std C++ namespace.
  static bool isInStdNamespace(const Decl *D);

private:
  std::unique_ptr<ManagedAnalysis> &getAnalysisImpl(const void *tag);

  LocationContextManager &getLocationContextManager();
};

/// It wraps the AnalysisDeclContext to represent both the call stack with
/// the help of StackFrameContext and inside the function calls the
/// BlockInvocationContext. It is needed for context sensitive analysis to
/// model entering, leaving or inlining function calls.
class LocationContext : public llvm::FoldingSetNode {
public:
  enum ContextKind { StackFrame, Block };

private:
  ContextKind Kind;

  // AnalysisDeclContext can't be const since some methods may modify its
  // member.
  AnalysisDeclContext *Ctx;

  const LocationContext *Parent;
  int64_t ID;

protected:
  LocationContext(ContextKind k, AnalysisDeclContext *ctx,
                  const LocationContext *parent, int64_t ID)
      : Kind(k), Ctx(ctx), Parent(parent), ID(ID) {}

public:
  virtual ~LocationContext();

  ContextKind getKind() const { return Kind; }

  int64_t getID() const { return ID; }

  AnalysisDeclContext *getAnalysisDeclContext() const { return Ctx; }

  const LocationContext *getParent() const { return Parent; }

  bool isParentOf(const LocationContext *LC) const;

  const Decl *getDecl() const { return Ctx->getDecl(); }

  CFG *getCFG() const { return Ctx->getCFG(); }

  template <typename T> T *getAnalysis() const { return Ctx->getAnalysis<T>(); }

  const ParentMap &getParentMap() const { return Ctx->getParentMap(); }

  /// \copydoc AnalysisDeclContext::getSelfDecl()
  const ImplicitParamDecl *getSelfDecl() const { return Ctx->getSelfDecl(); }

  const StackFrameContext *getStackFrame() const;

  /// \returns Whether the current LocationContext has no caller context.
  virtual bool inTopFrame() const;

  virtual void Profile(llvm::FoldingSetNodeID &ID) = 0;

  /// Prints out the call stack.
  ///
  /// \param Out The out stream.
  LLVM_DUMP_METHOD void dumpStack(raw_ostream &Out) const;

  /// Prints out the call stack in \c json format.
  ///
  /// \param Out   The out stream.
  /// \param NL    The newline.
  /// \param Space The space count for indentation.
  /// \param IsDot Whether the output format is \c dot.
  /// \param printMoreInfoPerContext
  /// A callback to print more information for each context, for example:
  /// \code
  ///   [&](const LocationContext *LC) { LC->dump(); }
  /// \endcode
  void printJson(
      raw_ostream &Out, const char *NL = "\n", unsigned int Space = 0,
      bool IsDot = false,
      std::function<void(const LocationContext *)> printMoreInfoPerContext =
          [](const LocationContext *) {}) const;

  LLVM_DUMP_METHOD void dump() const;

  static void ProfileCommon(llvm::FoldingSetNodeID &ID, ContextKind ck,
                            AnalysisDeclContext *ctx,
                            const LocationContext *parent, const void *data);
};

/// It represents a stack frame of the call stack (based on CallEvent).
class StackFrameContext : public LocationContext {
  friend class LocationContextManager;

  // The call site where this stack frame is established.
  const Stmt *CallSite;

  // The parent block of the call site.
  const CFGBlock *Block;

  // The number of times the 'Block' has been visited.
  // It allows discriminating between stack frames of the same call that is
  // called multiple times in a loop.
  const unsigned BlockCount;

  // The index of the call site in the CFGBlock.
  const unsigned Index;

  StackFrameContext(AnalysisDeclContext *ADC, const LocationContext *ParentLC,
                    const Stmt *S, const CFGBlock *Block, unsigned BlockCount,
                    unsigned Index, int64_t ID)
      : LocationContext(StackFrame, ADC, ParentLC, ID), CallSite(S),
        Block(Block), BlockCount(BlockCount), Index(Index) {}

public:
  ~StackFrameContext() override = default;

  const Stmt *getCallSite() const { return CallSite; }

  const CFGBlock *getCallSiteBlock() const { return Block; }

  bool inTopFrame() const override { return getParent() == nullptr; }

  unsigned getIndex() const { return Index; }

  CFGElement getCallSiteCFGElement() const { return (*Block)[Index]; }
  
  void Profile(llvm::FoldingSetNodeID &ID) override;

  static void Profile(llvm::FoldingSetNodeID &ID, AnalysisDeclContext *ADC,
                      const LocationContext *ParentLC, const Stmt *S,
                      const CFGBlock *Block, unsigned BlockCount,
                      unsigned Index) {
    ProfileCommon(ID, StackFrame, ADC, ParentLC, S);
    ID.AddPointer(Block);
    ID.AddInteger(BlockCount);
    ID.AddInteger(Index);
  }

  static bool classof(const LocationContext *LC) {
    return LC->getKind() == StackFrame;
  }
};

/// It represents a block invocation (based on BlockCall).
class BlockInvocationContext : public LocationContext {
  friend class LocationContextManager;

  const BlockDecl *BD;

  // FIXME: Come up with a more type-safe way to model context-sensitivity.
  const void *Data;

  BlockInvocationContext(AnalysisDeclContext *ADC,
                         const LocationContext *ParentLC, const BlockDecl *BD,
                         const void *Data, int64_t ID)
      : LocationContext(Block, ADC, ParentLC, ID), BD(BD), Data(Data) {}

public:
  ~BlockInvocationContext() override = default;

  const BlockDecl *getBlockDecl() const { return BD; }

  const void *getData() const { return Data; }

  void Profile(llvm::FoldingSetNodeID &ID) override;

  static void Profile(llvm::FoldingSetNodeID &ID, AnalysisDeclContext *ADC,
                      const LocationContext *ParentLC, const BlockDecl *BD,
                      const void *Data) {
    ProfileCommon(ID, Block, ADC, ParentLC, BD);
    ID.AddPointer(Data);
  }

  static bool classof(const LocationContext *LC) {
    return LC->getKind() == Block;
  }
};

class LocationContextManager {
  llvm::FoldingSet<LocationContext> Contexts;

  // ID used for generating a new location context.
  int64_t NewID = 0;

public:
  ~LocationContextManager();

  /// Obtain a context of the call stack using its parent context.
  ///
  /// \param ADC        The AnalysisDeclContext.
  /// \param ParentLC   The parent context of this newly created context.
  /// \param S          The call.
  /// \param Block      The basic block.
  /// \param BlockCount The current count of entering into \p Blk.
  /// \param Index      The index of \p Blk.
  /// \returns The context for \p D with parent context \p ParentLC.
  const StackFrameContext *getStackFrame(AnalysisDeclContext *ADC,
                                         const LocationContext *ParentLC,
                                         const Stmt *S, const CFGBlock *Block,
                                         unsigned BlockCount, unsigned Index);

  /// Obtain a context of the block invocation using its parent context.
  ///
  /// \param ADC      The AnalysisDeclContext.
  /// \param ParentLC The parent context of this newly created context.
  /// \param BD       The BlockDecl.
  /// \param Data     The raw data to store as part of the context.
  const BlockInvocationContext *
  getBlockInvocationContext(AnalysisDeclContext *ADC,
                            const LocationContext *ParentLC,
                            const BlockDecl *BD, const void *Data);

  /// Discard all previously created LocationContext objects.
  void clear();
};

class AnalysisDeclContextManager {
  using ContextMap =
      llvm::DenseMap<const Decl *, std::unique_ptr<AnalysisDeclContext>>;

  ContextMap Contexts;
  LocationContextManager LocCtxMgr;
  CFG::BuildOptions cfgBuildOptions;

  // Pointer to an interface that can provide function bodies for
  // declarations from external source.
  std::unique_ptr<CodeInjector> Injector;

  // A factory for creating and caching implementations for common
  // methods during the analysis.
  BodyFarm FunctionBodyFarm;

  // Flag to indicate whether or not bodies should be synthesized
  // for well-known functions.
  bool SynthesizeBodies;

public:
  AnalysisDeclContextManager(
      ASTContext &ASTCtx, bool useUnoptimizedCFG = false,
      bool addImplicitDtors = false, bool addInitializers = false,
      bool addTemporaryDtors = false, bool addLifetime = false,
      bool addLoopExit = false, bool addScopes = false,
      bool synthesizeBodies = false, bool addStaticInitBranches = false,
      bool addCXXNewAllocator = true, bool addRichCXXConstructors = true,
      bool markElidedCXXConstructors = true, bool addVirtualBaseBranches = true,
      CodeInjector *injector = nullptr);

  AnalysisDeclContext *getContext(const Decl *D);

  bool getUseUnoptimizedCFG() const {
    return !cfgBuildOptions.PruneTriviallyFalseEdges;
  }

  CFG::BuildOptions &getCFGBuildOptions() { return cfgBuildOptions; }

  /// \returns Whether faux bodies should be synthesized for known functions.
  bool synthesizeBodies() const { return SynthesizeBodies; }

  /// Obtain the beginning context of the analysis.
  ///
  /// \returns The top level stack frame for \p D.
  const StackFrameContext *getStackFrame(const Decl *D) {
    return LocCtxMgr.getStackFrame(getContext(D), nullptr, nullptr, nullptr, 0,
                                   0);
  }

  /// \copydoc LocationContextManager::getStackFrame()
  const StackFrameContext *getStackFrame(AnalysisDeclContext *ADC,
                                         const LocationContext *Parent,
                                         const Stmt *S, const CFGBlock *Block,
                                         unsigned BlockCount, unsigned Index) {
    return LocCtxMgr.getStackFrame(ADC, Parent, S, Block, BlockCount, Index);
  }

  BodyFarm &getBodyFarm();

  /// Discard all previously created AnalysisDeclContexts.
  void clear();

private:
  friend class AnalysisDeclContext;

  LocationContextManager &getLocationContextManager() { return LocCtxMgr; }
};

} // namespace clang

#endif // LLVM_CLANG_ANALYSIS_ANALYSISDECLCONTEXT_H
