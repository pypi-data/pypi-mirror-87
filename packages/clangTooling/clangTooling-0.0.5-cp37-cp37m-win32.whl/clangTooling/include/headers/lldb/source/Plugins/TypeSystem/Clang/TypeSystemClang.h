//===-- TypeSystemClang.h ---------------------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef LLDB_SOURCE_PLUGINS_TYPESYSTEM_CLANG_TYPESYSTEMCLANG_H
#define LLDB_SOURCE_PLUGINS_TYPESYSTEM_CLANG_TYPESYSTEMCLANG_H

#include <stdint.h>

#include <functional>
#include <initializer_list>
#include <map>
#include <memory>
#include <set>
#include <string>
#include <utility>
#include <vector>

#include "clang/AST/ASTContext.h"
#include "clang/AST/ASTFwd.h"
#include "clang/AST/TemplateBase.h"
#include "clang/Basic/TargetInfo.h"
#include "llvm/ADT/APSInt.h"
#include "llvm/ADT/SmallVector.h"

#include "Plugins/ExpressionParser/Clang/ClangPersistentVariables.h"
#include "lldb/Expression/ExpressionVariable.h"
#include "lldb/Symbol/CompilerType.h"
#include "lldb/Symbol/TypeSystem.h"
#include "lldb/Target/Target.h"
#include "lldb/Utility/ConstString.h"
#include "lldb/Utility/Flags.h"
#include "lldb/Utility/Log.h"
#include "lldb/Utility/Logging.h"
#include "lldb/lldb-enumerations.h"

class DWARFASTParserClang;
class PDBASTParser;

namespace clang {
class FileManager;
class HeaderSearch;
class ModuleMap;
} // namespace clang

namespace lldb_private {

class ClangASTMetadata;
class ClangASTSource;
class Declaration;

/// A Clang module ID.
class OptionalClangModuleID {
  unsigned m_id = 0;

public:
  OptionalClangModuleID() = default;
  explicit OptionalClangModuleID(unsigned id) : m_id(id) {}
  bool HasValue() const { return m_id != 0; }
  unsigned GetValue() const { return m_id; }
};

/// The implementation of lldb::Type's m_payload field for TypeSystemClang.
class TypePayloadClang {
  /// The Layout is as follows:
  /// \verbatim
  /// bit 0..30 ... Owning Module ID.
  /// bit 31 ...... IsCompleteObjCClass.
  /// \endverbatim
  Type::Payload m_payload = 0;

public:
  TypePayloadClang() = default;
  explicit TypePayloadClang(OptionalClangModuleID owning_module,
                            bool is_complete_objc_class = false);
  explicit TypePayloadClang(uint32_t opaque_payload) : m_payload(opaque_payload) {}
  operator Type::Payload() { return m_payload; }

  static constexpr unsigned ObjCClassBit = 1 << 31;
  bool IsCompleteObjCClass() { return Flags(m_payload).Test(ObjCClassBit); }
  void SetIsCompleteObjCClass(bool is_complete_objc_class) {
    m_payload = is_complete_objc_class ? Flags(m_payload).Set(ObjCClassBit)
                                       : Flags(m_payload).Clear(ObjCClassBit);
  }
  OptionalClangModuleID GetOwningModule() {
    return OptionalClangModuleID(Flags(m_payload).Clear(ObjCClassBit));
  }
  void SetOwningModule(OptionalClangModuleID id);
  /// \}
};
  
/// A TypeSystem implementation based on Clang.
///
/// This class uses a single clang::ASTContext as the backend for storing
/// its types and declarations. Every clang::ASTContext should also just have
/// a single associated TypeSystemClang instance that manages it.
///
/// The clang::ASTContext instance can either be created by TypeSystemClang
/// itself or it can adopt an existing clang::ASTContext (for example, when
/// it is necessary to provide a TypeSystem interface for an existing
/// clang::ASTContext that was created by clang::CompilerInstance).
class TypeSystemClang : public TypeSystem {
  // LLVM RTTI support
  static char ID;

public:
  typedef void (*CompleteTagDeclCallback)(void *baton, clang::TagDecl *);
  typedef void (*CompleteObjCInterfaceDeclCallback)(void *baton,
                                                    clang::ObjCInterfaceDecl *);

  // llvm casting support
  bool isA(const void *ClassID) const override { return ClassID == &ID; }
  static bool classof(const TypeSystem *ts) { return ts->isA(&ID); }

  /// Constructs a TypeSystemClang with an ASTContext using the given triple.
  ///
  /// \param name The name for the TypeSystemClang (for logging purposes)
  /// \param triple The llvm::Triple used for the ASTContext. The triple defines
  ///               certain characteristics of the ASTContext and its types
  ///               (e.g., whether certain primitive types exist or what their
  ///               signedness is).
  explicit TypeSystemClang(llvm::StringRef name, llvm::Triple triple);

  /// Constructs a TypeSystemClang that uses an existing ASTContext internally.
  /// Useful when having an existing ASTContext created by Clang.
  ///
  /// \param name The name for the TypeSystemClang (for logging purposes)
  /// \param existing_ctxt An existing ASTContext.
  explicit TypeSystemClang(llvm::StringRef name,
                           clang::ASTContext &existing_ctxt);

  ~TypeSystemClang() override;

  void Finalize() override;

  // PluginInterface functions
  ConstString GetPluginName() override;

  uint32_t GetPluginVersion() override;

  static ConstString GetPluginNameStatic();

  static lldb::TypeSystemSP CreateInstance(lldb::LanguageType language,
                                           Module *module, Target *target);

  static LanguageSet GetSupportedLanguagesForTypes();
  static LanguageSet GetSupportedLanguagesForExpressions();

  static void Initialize();

  static void Terminate();

  static TypeSystemClang *GetASTContext(clang::ASTContext *ast_ctx);

  static TypeSystemClang *GetScratch(Target &target,
                                     bool create_on_demand = true) {
    auto type_system_or_err = target.GetScratchTypeSystemForLanguage(
        lldb::eLanguageTypeC, create_on_demand);
    if (auto err = type_system_or_err.takeError()) {
      LLDB_LOG_ERROR(lldb_private::GetLogIfAnyCategoriesSet(LIBLLDB_LOG_TARGET),
                     std::move(err), "Couldn't get scratch TypeSystemClang");
      return nullptr;
    }
    return llvm::dyn_cast<TypeSystemClang>(&type_system_or_err.get());
  }

  /// Returns the display name of this TypeSystemClang that indicates what
  /// purpose it serves in LLDB. Used for example in logs.
  llvm::StringRef getDisplayName() const { return m_display_name; }

  /// Returns the clang::ASTContext instance managed by this TypeSystemClang.
  clang::ASTContext &getASTContext();

  clang::MangleContext *getMangleContext();

  std::shared_ptr<clang::TargetOptions> &getTargetOptions();

  clang::TargetInfo *getTargetInfo();

  void setSema(clang::Sema *s);
  clang::Sema *getSema() { return m_sema; }

  const char *GetTargetTriple();

  void SetExternalSource(
      llvm::IntrusiveRefCntPtr<clang::ExternalASTSource> &ast_source_up);

  bool GetCompleteDecl(clang::Decl *decl) {
    return TypeSystemClang::GetCompleteDecl(&getASTContext(), decl);
  }

  static void DumpDeclHiearchy(clang::Decl *decl);

  static void DumpDeclContextHiearchy(clang::DeclContext *decl_ctx);

  static bool DeclsAreEquivalent(clang::Decl *lhs_decl, clang::Decl *rhs_decl);

  static bool GetCompleteDecl(clang::ASTContext *ast, clang::Decl *decl);

  void SetMetadataAsUserID(const clang::Decl *decl, lldb::user_id_t user_id);
  void SetMetadataAsUserID(const clang::Type *type, lldb::user_id_t user_id);

  void SetMetadata(const clang::Decl *object, ClangASTMetadata &meta_data);

  void SetMetadata(const clang::Type *object, ClangASTMetadata &meta_data);
  ClangASTMetadata *GetMetadata(const clang::Decl *object);
  ClangASTMetadata *GetMetadata(const clang::Type *object);

  // Basic Types
  CompilerType GetBuiltinTypeForEncodingAndBitSize(lldb::Encoding encoding,
                                                   size_t bit_size) override;

  CompilerType GetBasicType(lldb::BasicType type);

  static lldb::BasicType GetBasicTypeEnumeration(ConstString name);

  CompilerType
  GetBuiltinTypeForDWARFEncodingAndBitSize(llvm::StringRef type_name,
                                           uint32_t dw_ate, uint32_t bit_size);

  CompilerType GetCStringType(bool is_const);

  static clang::DeclContext *GetDeclContextForType(clang::QualType type);

  static clang::DeclContext *GetDeclContextForType(const CompilerType &type);

  uint32_t GetPointerByteSize() override;

  clang::TranslationUnitDecl *GetTranslationUnitDecl() {
    return getASTContext().getTranslationUnitDecl();
  }

  static bool AreTypesSame(CompilerType type1, CompilerType type2,
                           bool ignore_qualifiers = false);

  /// Creates a CompilerType form the given QualType with the current
  /// TypeSystemClang instance as the CompilerType's typesystem.
  /// \param qt The QualType for a type that belongs to the ASTContext of this
  ///           TypeSystemClang.
  /// \return The CompilerType representing the given QualType. If the
  ///         QualType's type pointer is a nullptr then the function returns an
  ///         invalid CompilerType.
  CompilerType GetType(clang::QualType qt) {
    if (qt.getTypePtrOrNull() == nullptr)
      return CompilerType();
    // Check that the type actually belongs to this TypeSystemClang.
    assert(qt->getAsTagDecl() == nullptr ||
           &qt->getAsTagDecl()->getASTContext() == &getASTContext());
    return CompilerType(this, qt.getAsOpaquePtr());
  }

  CompilerType GetTypeForDecl(clang::NamedDecl *decl);

  CompilerType GetTypeForDecl(clang::TagDecl *decl);

  CompilerType GetTypeForDecl(clang::ObjCInterfaceDecl *objc_decl);

  template <typename RecordDeclType>
  CompilerType
  GetTypeForIdentifier(ConstString type_name,
                       clang::DeclContext *decl_context = nullptr) {
    CompilerType compiler_type;

    if (type_name.GetLength()) {
      clang::ASTContext &ast = getASTContext();
      if (!decl_context)
        decl_context = ast.getTranslationUnitDecl();

      clang::IdentifierInfo &myIdent = ast.Idents.get(type_name.GetCString());
      clang::DeclarationName myName =
          ast.DeclarationNames.getIdentifier(&myIdent);

      clang::DeclContext::lookup_result result = decl_context->lookup(myName);

      if (!result.empty()) {
        clang::NamedDecl *named_decl = result[0];
        if (const RecordDeclType *record_decl =
                llvm::dyn_cast<RecordDeclType>(named_decl))
          compiler_type.SetCompilerType(
              this, clang::QualType(record_decl->getTypeForDecl(), 0)
                        .getAsOpaquePtr());
      }
    }

    return compiler_type;
  }

  CompilerType CreateStructForIdentifier(
      ConstString type_name,
      const std::initializer_list<std::pair<const char *, CompilerType>>
          &type_fields,
      bool packed = false);

  CompilerType GetOrCreateStructForIdentifier(
      ConstString type_name,
      const std::initializer_list<std::pair<const char *, CompilerType>>
          &type_fields,
      bool packed = false);

  static bool IsOperator(llvm::StringRef name,
                         clang::OverloadedOperatorKind &op_kind);

  // Structure, Unions, Classes

  static clang::AccessSpecifier
  ConvertAccessTypeToAccessSpecifier(lldb::AccessType access);

  static clang::AccessSpecifier
  UnifyAccessSpecifiers(clang::AccessSpecifier lhs, clang::AccessSpecifier rhs);

  static uint32_t GetNumBaseClasses(const clang::CXXRecordDecl *cxx_record_decl,
                                    bool omit_empty_base_classes);

  /// Synthesize a clang::Module and return its ID or a default-constructed ID.
  OptionalClangModuleID GetOrCreateClangModule(llvm::StringRef name,
                                               OptionalClangModuleID parent,
                                               bool is_framework = false,
                                               bool is_explicit = false);

  CompilerType CreateRecordType(clang::DeclContext *decl_ctx,
                                OptionalClangModuleID owning_module,
                                lldb::AccessType access_type,
                                llvm::StringRef name, int kind,
                                lldb::LanguageType language,
                                ClangASTMetadata *metadata = nullptr,
                                bool exports_symbols = false);

  class TemplateParameterInfos {
  public:
    bool IsValid() const {
      if (args.empty())
        return false;
      return args.size() == names.size() &&
        ((bool)pack_name == (bool)packed_args) &&
        (!packed_args || !packed_args->packed_args);
    }

    llvm::SmallVector<const char *, 2> names;
    llvm::SmallVector<clang::TemplateArgument, 2> args;
    
    const char * pack_name = nullptr;
    std::unique_ptr<TemplateParameterInfos> packed_args;
  };

  clang::FunctionTemplateDecl *CreateFunctionTemplateDecl(
      clang::DeclContext *decl_ctx, OptionalClangModuleID owning_module,
      clang::FunctionDecl *func_decl, const TemplateParameterInfos &infos);

  void CreateFunctionTemplateSpecializationInfo(
      clang::FunctionDecl *func_decl, clang::FunctionTemplateDecl *Template,
      const TemplateParameterInfos &infos);

  clang::ClassTemplateDecl *
  CreateClassTemplateDecl(clang::DeclContext *decl_ctx,
                          OptionalClangModuleID owning_module,
                          lldb::AccessType access_type, const char *class_name,
                          int kind, const TemplateParameterInfos &infos);

  clang::TemplateTemplateParmDecl *
  CreateTemplateTemplateParmDecl(const char *template_name);

  clang::ClassTemplateSpecializationDecl *CreateClassTemplateSpecializationDecl(
      clang::DeclContext *decl_ctx, OptionalClangModuleID owning_module,
      clang::ClassTemplateDecl *class_template_decl, int kind,
      const TemplateParameterInfos &infos);

  CompilerType
  CreateClassTemplateSpecializationType(clang::ClassTemplateSpecializationDecl *
                                            class_template_specialization_decl);

  static clang::DeclContext *
  GetAsDeclContext(clang::FunctionDecl *function_decl);

  static bool CheckOverloadedOperatorKindParameterCount(
      bool is_method, clang::OverloadedOperatorKind op_kind,
      uint32_t num_params);

  bool FieldIsBitfield(clang::FieldDecl *field, uint32_t &bitfield_bit_size);

  static bool RecordHasFields(const clang::RecordDecl *record_decl);

  CompilerType CreateObjCClass(llvm::StringRef name,
                               clang::DeclContext *decl_ctx,
                               OptionalClangModuleID owning_module,
                               bool isForwardDecl, bool isInternal,
                               ClangASTMetadata *metadata = nullptr);

  bool SetTagTypeKind(clang::QualType type, int kind) const;

  bool SetDefaultAccessForRecordFields(clang::RecordDecl *record_decl,
                                       int default_accessibility,
                                       int *assigned_accessibilities,
                                       size_t num_assigned_accessibilities);

  // Returns a mask containing bits from the TypeSystemClang::eTypeXXX
  // enumerations

  // Namespace Declarations

  clang::NamespaceDecl *
  GetUniqueNamespaceDeclaration(const char *name, clang::DeclContext *decl_ctx,
                                OptionalClangModuleID owning_module,
                                bool is_inline = false);

  // Function Types

  clang::FunctionDecl *CreateFunctionDeclaration(
      clang::DeclContext *decl_ctx, OptionalClangModuleID owning_module,
      llvm::StringRef name, const CompilerType &function_Type,
      clang::StorageClass storage, bool is_inline);

  CompilerType CreateFunctionType(const CompilerType &result_type,
                                  const CompilerType *args, unsigned num_args,
                                  bool is_variadic, unsigned type_quals,
                                  clang::CallingConv cc);

  CompilerType CreateFunctionType(const CompilerType &result_type,
                                  const CompilerType *args, unsigned num_args,
                                  bool is_variadic, unsigned type_quals) {
    return CreateFunctionType(result_type, args, num_args, is_variadic,
                              type_quals, clang::CC_C);
  }

  clang::ParmVarDecl *
  CreateParameterDeclaration(clang::DeclContext *decl_ctx,
                             OptionalClangModuleID owning_module,
                             const char *name, const CompilerType &param_type,
                             int storage, bool add_decl = false);

  void SetFunctionParameters(clang::FunctionDecl *function_decl,
                             clang::ParmVarDecl **params, unsigned num_params);

  CompilerType CreateBlockPointerType(const CompilerType &function_type);

  // Array Types

  CompilerType CreateArrayType(const CompilerType &element_type,
                               size_t element_count, bool is_vector);

  // Enumeration Types
  CompilerType CreateEnumerationType(const char *name,
                                     clang::DeclContext *decl_ctx,
                                     OptionalClangModuleID owning_module,
                                     const Declaration &decl,
                                     const CompilerType &integer_qual_type,
                                     bool is_scoped);

  // Integer type functions

  CompilerType GetIntTypeFromBitSize(size_t bit_size, bool is_signed);

  CompilerType GetPointerSizedIntType(bool is_signed);

  // Floating point functions

  static CompilerType GetFloatTypeFromBitSize(clang::ASTContext *ast,
                                              size_t bit_size);

  // TypeSystem methods
  DWARFASTParser *GetDWARFParser() override;
  PDBASTParser *GetPDBParser() override;

  // TypeSystemClang callbacks for external source lookups.
  void CompleteTagDecl(clang::TagDecl *);

  void CompleteObjCInterfaceDecl(clang::ObjCInterfaceDecl *);

  bool LayoutRecordType(
      const clang::RecordDecl *record_decl, uint64_t &size, uint64_t &alignment,
      llvm::DenseMap<const clang::FieldDecl *, uint64_t> &field_offsets,
      llvm::DenseMap<const clang::CXXRecordDecl *, clang::CharUnits>
          &base_offsets,
      llvm::DenseMap<const clang::CXXRecordDecl *, clang::CharUnits>
          &vbase_offsets);

  /// Creates a CompilerDecl from the given Decl with the current
  /// TypeSystemClang instance as its typesystem.
  /// The Decl has to come from the ASTContext of this
  /// TypeSystemClang.
  CompilerDecl GetCompilerDecl(clang::Decl *decl) {
    assert(&decl->getASTContext() == &getASTContext() &&
           "CreateCompilerDecl for Decl from wrong ASTContext?");
    return CompilerDecl(this, decl);
  }

  // CompilerDecl override functions
  ConstString DeclGetName(void *opaque_decl) override;

  ConstString DeclGetMangledName(void *opaque_decl) override;

  CompilerDeclContext DeclGetDeclContext(void *opaque_decl) override;

  CompilerType DeclGetFunctionReturnType(void *opaque_decl) override;

  size_t DeclGetFunctionNumArguments(void *opaque_decl) override;

  CompilerType DeclGetFunctionArgumentType(void *opaque_decl,
                                           size_t arg_idx) override;

  CompilerType GetTypeForDecl(void *opaque_decl) override;

  // CompilerDeclContext override functions

  /// Creates a CompilerDeclContext from the given DeclContext
  /// with the current TypeSystemClang instance as its typesystem.
  /// The DeclContext has to come from the ASTContext of this
  /// TypeSystemClang.
  CompilerDeclContext CreateDeclContext(clang::DeclContext *ctx);

  /// Set the owning module for \p decl.
  static void SetOwningModule(clang::Decl *decl,
                              OptionalClangModuleID owning_module);

  std::vector<CompilerDecl>
  DeclContextFindDeclByName(void *opaque_decl_ctx, ConstString name,
                            const bool ignore_using_decls) override;

  ConstString DeclContextGetName(void *opaque_decl_ctx) override;

  ConstString DeclContextGetScopeQualifiedName(void *opaque_decl_ctx) override;

  bool DeclContextIsClassMethod(void *opaque_decl_ctx,
                                lldb::LanguageType *language_ptr,
                                bool *is_instance_method_ptr,
                                ConstString *language_object_name_ptr) override;

  bool DeclContextIsContainedInLookup(void *opaque_decl_ctx,
                                      void *other_opaque_decl_ctx) override;

  // Clang specific clang::DeclContext functions

  static clang::DeclContext *
  DeclContextGetAsDeclContext(const CompilerDeclContext &dc);

  static clang::ObjCMethodDecl *
  DeclContextGetAsObjCMethodDecl(const CompilerDeclContext &dc);

  static clang::CXXMethodDecl *
  DeclContextGetAsCXXMethodDecl(const CompilerDeclContext &dc);

  static clang::FunctionDecl *
  DeclContextGetAsFunctionDecl(const CompilerDeclContext &dc);

  static clang::NamespaceDecl *
  DeclContextGetAsNamespaceDecl(const CompilerDeclContext &dc);

  static ClangASTMetadata *DeclContextGetMetaData(const CompilerDeclContext &dc,
                                                  const clang::Decl *object);

  static clang::ASTContext *
  DeclContextGetTypeSystemClang(const CompilerDeclContext &dc);

  // Tests

#ifndef NDEBUG
  bool Verify(lldb::opaque_compiler_type_t type) override;
#endif
  
  bool IsArrayType(lldb::opaque_compiler_type_t type,
                   CompilerType *element_type, uint64_t *size,
                   bool *is_incomplete) override;

  bool IsVectorType(lldb::opaque_compiler_type_t type,
                    CompilerType *element_type, uint64_t *size) override;

  bool IsAggregateType(lldb::opaque_compiler_type_t type) override;

  bool IsAnonymousType(lldb::opaque_compiler_type_t type) override;

  bool IsBeingDefined(lldb::opaque_compiler_type_t type) override;

  bool IsCharType(lldb::opaque_compiler_type_t type) override;

  bool IsCompleteType(lldb::opaque_compiler_type_t type) override;

  bool IsConst(lldb::opaque_compiler_type_t type) override;

  bool IsCStringType(lldb::opaque_compiler_type_t type,
                     uint32_t &length) override;

  static bool IsCXXClassType(const CompilerType &type);

  bool IsDefined(lldb::opaque_compiler_type_t type) override;

  bool IsFloatingPointType(lldb::opaque_compiler_type_t type, uint32_t &count,
                           bool &is_complex) override;

  bool IsFunctionType(lldb::opaque_compiler_type_t type,
                      bool *is_variadic_ptr) override;

  uint32_t IsHomogeneousAggregate(lldb::opaque_compiler_type_t type,
                                  CompilerType *base_type_ptr) override;

  size_t
  GetNumberOfFunctionArguments(lldb::opaque_compiler_type_t type) override;

  CompilerType GetFunctionArgumentAtIndex(lldb::opaque_compiler_type_t type,
                                          const size_t index) override;

  bool IsFunctionPointerType(lldb::opaque_compiler_type_t type) override;

  bool IsBlockPointerType(lldb::opaque_compiler_type_t type,
                          CompilerType *function_pointer_type_ptr) override;

  bool IsIntegerType(lldb::opaque_compiler_type_t type,
                     bool &is_signed) override;

  bool IsEnumerationType(lldb::opaque_compiler_type_t type,
                         bool &is_signed) override;

  static bool IsObjCClassType(const CompilerType &type);

  static bool IsObjCClassTypeAndHasIVars(const CompilerType &type,
                                         bool check_superclass);

  static bool IsObjCObjectOrInterfaceType(const CompilerType &type);

  static bool IsObjCObjectPointerType(const CompilerType &type,
                                      CompilerType *target_type = nullptr);

  bool IsPolymorphicClass(lldb::opaque_compiler_type_t type) override;

  static bool IsClassType(lldb::opaque_compiler_type_t type);

  static bool IsEnumType(lldb::opaque_compiler_type_t type);

  bool IsPossibleDynamicType(lldb::opaque_compiler_type_t type,
                             CompilerType *target_type, // Can pass nullptr
                             bool check_cplusplus, bool check_objc) override;

  bool IsRuntimeGeneratedType(lldb::opaque_compiler_type_t type) override;

  bool IsPointerType(lldb::opaque_compiler_type_t type,
                     CompilerType *pointee_type) override;

  bool IsPointerOrReferenceType(lldb::opaque_compiler_type_t type,
                                CompilerType *pointee_type) override;

  bool IsReferenceType(lldb::opaque_compiler_type_t type,
                       CompilerType *pointee_type, bool *is_rvalue) override;

  bool IsScalarType(lldb::opaque_compiler_type_t type) override;

  bool IsTypedefType(lldb::opaque_compiler_type_t type) override;

  bool IsVoidType(lldb::opaque_compiler_type_t type) override;

  bool CanPassInRegisters(const CompilerType &type) override;

  bool SupportsLanguage(lldb::LanguageType language) override;

  static llvm::Optional<std::string> GetCXXClassName(const CompilerType &type);

  // Type Completion

  bool GetCompleteType(lldb::opaque_compiler_type_t type) override;

  // Accessors

  ConstString GetTypeName(lldb::opaque_compiler_type_t type) override;

  ConstString GetDisplayTypeName(lldb::opaque_compiler_type_t type) override;

  uint32_t GetTypeInfo(lldb::opaque_compiler_type_t type,
                       CompilerType *pointee_or_element_compiler_type) override;

  lldb::LanguageType
  GetMinimumLanguage(lldb::opaque_compiler_type_t type) override;

  lldb::TypeClass GetTypeClass(lldb::opaque_compiler_type_t type) override;

  unsigned GetTypeQualifiers(lldb::opaque_compiler_type_t type) override;

  // Creating related types

  /// Using the current type, create a new typedef to that type using
  /// "typedef_name" as the name and "decl_ctx" as the decl context.
  /// \param opaque_payload is an opaque TypePayloadClang.
  static CompilerType
  CreateTypedefType(const CompilerType &type, const char *typedef_name,
                    const CompilerDeclContext &compiler_decl_ctx,
                    uint32_t opaque_payload);

  CompilerType GetArrayElementType(lldb::opaque_compiler_type_t type,
                                   ExecutionContextScope *exe_scope) override;

  CompilerType GetArrayType(lldb::opaque_compiler_type_t type,
                            uint64_t size) override;

  CompilerType GetCanonicalType(lldb::opaque_compiler_type_t type) override;

  CompilerType
  GetFullyUnqualifiedType(lldb::opaque_compiler_type_t type) override;

  // Returns -1 if this isn't a function of if the function doesn't have a
  // prototype Returns a value >= 0 if there is a prototype.
  int GetFunctionArgumentCount(lldb::opaque_compiler_type_t type) override;

  CompilerType GetFunctionArgumentTypeAtIndex(lldb::opaque_compiler_type_t type,
                                              size_t idx) override;

  CompilerType
  GetFunctionReturnType(lldb::opaque_compiler_type_t type) override;

  size_t GetNumMemberFunctions(lldb::opaque_compiler_type_t type) override;

  TypeMemberFunctionImpl
  GetMemberFunctionAtIndex(lldb::opaque_compiler_type_t type,
                           size_t idx) override;

  CompilerType GetNonReferenceType(lldb::opaque_compiler_type_t type) override;

  CompilerType GetPointeeType(lldb::opaque_compiler_type_t type) override;

  CompilerType GetPointerType(lldb::opaque_compiler_type_t type) override;

  CompilerType
  GetLValueReferenceType(lldb::opaque_compiler_type_t type) override;

  CompilerType
  GetRValueReferenceType(lldb::opaque_compiler_type_t type) override;

  CompilerType GetAtomicType(lldb::opaque_compiler_type_t type) override;

  CompilerType AddConstModifier(lldb::opaque_compiler_type_t type) override;

  CompilerType AddVolatileModifier(lldb::opaque_compiler_type_t type) override;

  CompilerType AddRestrictModifier(lldb::opaque_compiler_type_t type) override;

  CompilerType CreateTypedef(lldb::opaque_compiler_type_t type,
                             const char *name,
                             const CompilerDeclContext &decl_ctx,
                             uint32_t opaque_payload) override;

  // If the current object represents a typedef type, get the underlying type
  CompilerType GetTypedefedType(lldb::opaque_compiler_type_t type) override;

  // Create related types using the current type's AST
  CompilerType GetBasicTypeFromAST(lldb::BasicType basic_type) override;

  // Exploring the type

  const llvm::fltSemantics &GetFloatTypeSemantics(size_t byte_size) override;

  llvm::Optional<uint64_t> GetByteSize(lldb::opaque_compiler_type_t type,
                       ExecutionContextScope *exe_scope) {
    if (llvm::Optional<uint64_t> bit_size = GetBitSize(type, exe_scope))
      return (*bit_size + 7) / 8;
    return llvm::None;
  }

  llvm::Optional<uint64_t>
  GetBitSize(lldb::opaque_compiler_type_t type,
             ExecutionContextScope *exe_scope) override;

  lldb::Encoding GetEncoding(lldb::opaque_compiler_type_t type,
                             uint64_t &count) override;

  lldb::Format GetFormat(lldb::opaque_compiler_type_t type) override;

  llvm::Optional<size_t>
  GetTypeBitAlign(lldb::opaque_compiler_type_t type,
                  ExecutionContextScope *exe_scope) override;

  uint32_t GetNumChildren(lldb::opaque_compiler_type_t type,
                          bool omit_empty_base_classes,
                          const ExecutionContext *exe_ctx) override;

  CompilerType GetBuiltinTypeByName(ConstString name) override;

  lldb::BasicType
  GetBasicTypeEnumeration(lldb::opaque_compiler_type_t type) override;

  static lldb::BasicType
  GetBasicTypeEnumeration(lldb::opaque_compiler_type_t type,
                          ConstString name);

  void ForEachEnumerator(
      lldb::opaque_compiler_type_t type,
      std::function<bool(const CompilerType &integer_type,
                         ConstString name,
                         const llvm::APSInt &value)> const &callback) override;

  uint32_t GetNumFields(lldb::opaque_compiler_type_t type) override;

  CompilerType GetFieldAtIndex(lldb::opaque_compiler_type_t type, size_t idx,
                               std::string &name, uint64_t *bit_offset_ptr,
                               uint32_t *bitfield_bit_size_ptr,
                               bool *is_bitfield_ptr) override;

  uint32_t GetNumDirectBaseClasses(lldb::opaque_compiler_type_t type) override;

  uint32_t GetNumVirtualBaseClasses(lldb::opaque_compiler_type_t type) override;

  CompilerType GetDirectBaseClassAtIndex(lldb::opaque_compiler_type_t type,
                                         size_t idx,
                                         uint32_t *bit_offset_ptr) override;

  CompilerType GetVirtualBaseClassAtIndex(lldb::opaque_compiler_type_t type,
                                          size_t idx,
                                          uint32_t *bit_offset_ptr) override;

  static uint32_t GetNumPointeeChildren(clang::QualType type);

  CompilerType GetChildCompilerTypeAtIndex(
      lldb::opaque_compiler_type_t type, ExecutionContext *exe_ctx, size_t idx,
      bool transparent_pointers, bool omit_empty_base_classes,
      bool ignore_array_bounds, std::string &child_name,
      uint32_t &child_byte_size, int32_t &child_byte_offset,
      uint32_t &child_bitfield_bit_size, uint32_t &child_bitfield_bit_offset,
      bool &child_is_base_class, bool &child_is_deref_of_parent,
      ValueObject *valobj, uint64_t &language_flags) override;

  // Lookup a child given a name. This function will match base class names and
  // member member names in "clang_type" only, not descendants.
  uint32_t GetIndexOfChildWithName(lldb::opaque_compiler_type_t type,
                                   const char *name,
                                   bool omit_empty_base_classes) override;

  // Lookup a child member given a name. This function will match member names
  // only and will descend into "clang_type" children in search for the first
  // member in this class, or any base class that matches "name".
  // TODO: Return all matches for a given name by returning a
  // vector<vector<uint32_t>>
  // so we catch all names that match a given child name, not just the first.
  size_t
  GetIndexOfChildMemberWithName(lldb::opaque_compiler_type_t type,
                                const char *name, bool omit_empty_base_classes,
                                std::vector<uint32_t> &child_indexes) override;

  size_t GetNumTemplateArguments(lldb::opaque_compiler_type_t type) override;

  lldb::TemplateArgumentKind
  GetTemplateArgumentKind(lldb::opaque_compiler_type_t type,
                          size_t idx) override;
  CompilerType GetTypeTemplateArgument(lldb::opaque_compiler_type_t type,
                                       size_t idx) override;
  llvm::Optional<CompilerType::IntegralTemplateArgument>
  GetIntegralTemplateArgument(lldb::opaque_compiler_type_t type,
                              size_t idx) override;

  CompilerType GetTypeForFormatters(void *type) override;

#define LLDB_INVALID_DECL_LEVEL UINT32_MAX
  // LLDB_INVALID_DECL_LEVEL is returned by CountDeclLevels if child_decl_ctx
  // could not be found in decl_ctx.
  uint32_t CountDeclLevels(clang::DeclContext *frame_decl_ctx,
                           clang::DeclContext *child_decl_ctx,
                           ConstString *child_name = nullptr,
                           CompilerType *child_type = nullptr);

  // Modifying RecordType
  static clang::FieldDecl *AddFieldToRecordType(const CompilerType &type,
                                                llvm::StringRef name,
                                                const CompilerType &field_type,
                                                lldb::AccessType access,
                                                uint32_t bitfield_bit_size);

  static void BuildIndirectFields(const CompilerType &type);

  static void SetIsPacked(const CompilerType &type);

  static clang::VarDecl *AddVariableToRecordType(const CompilerType &type,
                                                 llvm::StringRef name,
                                                 const CompilerType &var_type,
                                                 lldb::AccessType access);

  /// Initializes a variable with an integer value.
  /// \param var The variable to initialize. Must not already have an
  ///            initializer and must have an integer or enum type.
  /// \param init_value The integer value that the variable should be
  ///                   initialized to. Has to match the bit width of the
  ///                   variable type.
  static void SetIntegerInitializerForVariable(clang::VarDecl *var,
                                               const llvm::APInt &init_value);

  /// Initializes a variable with a floating point value.
  /// \param var The variable to initialize. Must not already have an
  ///            initializer and must have a floating point type.
  /// \param init_value The float value that the variable should be
  ///                   initialized to.
  static void
  SetFloatingInitializerForVariable(clang::VarDecl *var,
                                    const llvm::APFloat &init_value);

  clang::CXXMethodDecl *AddMethodToCXXRecordType(
      lldb::opaque_compiler_type_t type, llvm::StringRef name,
      const char *mangled_name, const CompilerType &method_type,
      lldb::AccessType access, bool is_virtual, bool is_static, bool is_inline,
      bool is_explicit, bool is_attr_used, bool is_artificial);

  void AddMethodOverridesForCXXRecordType(lldb::opaque_compiler_type_t type);

  // C++ Base Classes
  std::unique_ptr<clang::CXXBaseSpecifier>
  CreateBaseClassSpecifier(lldb::opaque_compiler_type_t type,
                           lldb::AccessType access, bool is_virtual,
                           bool base_of_class);

  bool TransferBaseClasses(
      lldb::opaque_compiler_type_t type,
      std::vector<std::unique_ptr<clang::CXXBaseSpecifier>> bases);

  static bool SetObjCSuperClass(const CompilerType &type,
                                const CompilerType &superclass_compiler_type);

  static bool AddObjCClassProperty(const CompilerType &type,
                                   const char *property_name,
                                   const CompilerType &property_compiler_type,
                                   clang::ObjCIvarDecl *ivar_decl,
                                   const char *property_setter_name,
                                   const char *property_getter_name,
                                   uint32_t property_attributes,
                                   ClangASTMetadata *metadata);

  static clang::ObjCMethodDecl *AddMethodToObjCObjectType(
      const CompilerType &type,
      const char *name, // the full symbol name as seen in the symbol table
                        // (lldb::opaque_compiler_type_t type, "-[NString
                        // stringWithCString:]")
      const CompilerType &method_compiler_type, lldb::AccessType access,
      bool is_artificial, bool is_variadic, bool is_objc_direct_call);

  static bool SetHasExternalStorage(lldb::opaque_compiler_type_t type,
                                    bool has_extern);

  // Tag Declarations
  static bool StartTagDeclarationDefinition(const CompilerType &type);

  static bool CompleteTagDeclarationDefinition(const CompilerType &type);

  // Modifying Enumeration types
  clang::EnumConstantDecl *AddEnumerationValueToEnumerationType(
      const CompilerType &enum_type, const Declaration &decl, const char *name,
      int64_t enum_value, uint32_t enum_value_bit_size);
  clang::EnumConstantDecl *AddEnumerationValueToEnumerationType(
      const CompilerType &enum_type, const Declaration &decl, const char *name,
      const llvm::APSInt &value);

  /// Returns the underlying integer type for an enum type. If the given type
  /// is invalid or not an enum-type, the function returns an invalid
  /// CompilerType.
  CompilerType GetEnumerationIntegerType(CompilerType type);

  // Pointers & References

  // Call this function using the class type when you want to make a member
  // pointer type to pointee_type.
  static CompilerType CreateMemberPointerType(const CompilerType &type,
                                              const CompilerType &pointee_type);

  // Dumping types
#ifndef NDEBUG
  /// Convenience LLVM-style dump method for use in the debugger only.
  /// In contrast to the other \p Dump() methods this directly invokes
  /// \p clang::QualType::dump().
  LLVM_DUMP_METHOD void dump(lldb::opaque_compiler_type_t type) const override;
#endif

  void Dump(Stream &s);

  /// Dump clang AST types from the symbol file.
  ///
  /// \param[in] s
  ///       A stream to send the dumped AST node(s) to
  /// \param[in] symbol_name
  ///       The name of the symbol to dump, if it is empty dump all the symbols
  void DumpFromSymbolFile(Stream &s, llvm::StringRef symbol_name);

  void DumpValue(lldb::opaque_compiler_type_t type, ExecutionContext *exe_ctx,
                 Stream *s, lldb::Format format, const DataExtractor &data,
                 lldb::offset_t data_offset, size_t data_byte_size,
                 uint32_t bitfield_bit_size, uint32_t bitfield_bit_offset,
                 bool show_types, bool show_summary, bool verbose,
                 uint32_t depth) override;

  bool DumpTypeValue(lldb::opaque_compiler_type_t type, Stream *s,
                     lldb::Format format, const DataExtractor &data,
                     lldb::offset_t data_offset, size_t data_byte_size,
                     uint32_t bitfield_bit_size, uint32_t bitfield_bit_offset,
                     ExecutionContextScope *exe_scope) override;

  void DumpSummary(lldb::opaque_compiler_type_t type, ExecutionContext *exe_ctx,
                   Stream *s, const DataExtractor &data,
                   lldb::offset_t data_offset, size_t data_byte_size) override;

  void DumpTypeDescription(
      lldb::opaque_compiler_type_t type,
      lldb::DescriptionLevel level = lldb::eDescriptionLevelFull) override;

  void DumpTypeDescription(
      lldb::opaque_compiler_type_t type, Stream *s,
      lldb::DescriptionLevel level = lldb::eDescriptionLevelFull) override;

  static void DumpTypeName(const CompilerType &type);

  static clang::EnumDecl *GetAsEnumDecl(const CompilerType &type);

  static clang::RecordDecl *GetAsRecordDecl(const CompilerType &type);

  static clang::TagDecl *GetAsTagDecl(const CompilerType &type);

  static clang::TypedefNameDecl *GetAsTypedefDecl(const CompilerType &type);

  static clang::CXXRecordDecl *
  GetAsCXXRecordDecl(lldb::opaque_compiler_type_t type);

  static clang::ObjCInterfaceDecl *
  GetAsObjCInterfaceDecl(const CompilerType &type);

  clang::ClassTemplateDecl *ParseClassTemplateDecl(
      clang::DeclContext *decl_ctx, OptionalClangModuleID owning_module,
      lldb::AccessType access_type, const char *parent_name, int tag_decl_kind,
      const TypeSystemClang::TemplateParameterInfos &template_param_infos);

  clang::BlockDecl *CreateBlockDeclaration(clang::DeclContext *ctx,
                                           OptionalClangModuleID owning_module);

  clang::UsingDirectiveDecl *
  CreateUsingDirectiveDeclaration(clang::DeclContext *decl_ctx,
                                  OptionalClangModuleID owning_module,
                                  clang::NamespaceDecl *ns_decl);

  clang::UsingDecl *CreateUsingDeclaration(clang::DeclContext *current_decl_ctx,
                                           OptionalClangModuleID owning_module,
                                           clang::NamedDecl *target);

  clang::VarDecl *CreateVariableDeclaration(clang::DeclContext *decl_context,
                                            OptionalClangModuleID owning_module,
                                            const char *name,
                                            clang::QualType type);

  static lldb::opaque_compiler_type_t
  GetOpaqueCompilerType(clang::ASTContext *ast, lldb::BasicType basic_type);

  static clang::QualType GetQualType(lldb::opaque_compiler_type_t type) {
    if (type)
      return clang::QualType::getFromOpaquePtr(type);
    return clang::QualType();
  }

  static clang::QualType
  GetCanonicalQualType(lldb::opaque_compiler_type_t type) {
    if (type)
      return clang::QualType::getFromOpaquePtr(type).getCanonicalType();
    return clang::QualType();
  }

  clang::DeclarationName
  GetDeclarationName(llvm::StringRef name,
                     const CompilerType &function_clang_type);

  clang::LangOptions *GetLangOpts() const {
    return m_language_options_up.get();
  }
  clang::SourceManager *GetSourceMgr() const {
    return m_source_manager_up.get();
  }

private:
  const clang::ClassTemplateSpecializationDecl *
  GetAsTemplateSpecialization(lldb::opaque_compiler_type_t type);

  // Classes that inherit from TypeSystemClang can see and modify these
  std::string m_target_triple;
  std::unique_ptr<clang::ASTContext> m_ast_up;
  std::unique_ptr<clang::LangOptions> m_language_options_up;
  std::unique_ptr<clang::FileManager> m_file_manager_up;
  std::unique_ptr<clang::SourceManager> m_source_manager_up;
  std::unique_ptr<clang::DiagnosticsEngine> m_diagnostics_engine_up;
  std::unique_ptr<clang::DiagnosticConsumer> m_diagnostic_consumer_up;
  std::shared_ptr<clang::TargetOptions> m_target_options_rp;
  std::unique_ptr<clang::TargetInfo> m_target_info_up;
  std::unique_ptr<clang::IdentifierTable> m_identifier_table_up;
  std::unique_ptr<clang::SelectorTable> m_selector_table_up;
  std::unique_ptr<clang::Builtin::Context> m_builtins_up;
  std::unique_ptr<clang::HeaderSearch> m_header_search_up;
  std::unique_ptr<clang::ModuleMap> m_module_map_up;
  std::unique_ptr<DWARFASTParserClang> m_dwarf_ast_parser_up;
  std::unique_ptr<PDBASTParser> m_pdb_ast_parser_up;
  std::unique_ptr<clang::MangleContext> m_mangle_ctx_up;
  uint32_t m_pointer_byte_size = 0;
  bool m_ast_owned = false;
  /// A string describing what this TypeSystemClang represents (e.g.,
  /// AST for debug information, an expression, some other utility ClangAST).
  /// Useful for logging and debugging.
  std::string m_display_name;

  typedef llvm::DenseMap<const clang::Decl *, ClangASTMetadata> DeclMetadataMap;
  /// Maps Decls to their associated ClangASTMetadata.
  DeclMetadataMap m_decl_metadata;

  typedef llvm::DenseMap<const clang::Type *, ClangASTMetadata> TypeMetadataMap;
  /// Maps Types to their associated ClangASTMetadata.
  TypeMetadataMap m_type_metadata;

  /// The sema associated that is currently used to build this ASTContext.
  /// May be null if we are already done parsing this ASTContext or the
  /// ASTContext wasn't created by parsing source code.
  clang::Sema *m_sema = nullptr;

  // For TypeSystemClang only
  TypeSystemClang(const TypeSystemClang &);
  const TypeSystemClang &operator=(const TypeSystemClang &);
  /// Creates the internal ASTContext.
  void CreateASTContext();
  void SetTargetTriple(llvm::StringRef target_triple);
};

/// The TypeSystemClang instance used for the scratch ASTContext in a
/// lldb::Target.
class TypeSystemClangForExpressions : public TypeSystemClang {
public:
  TypeSystemClangForExpressions(Target &target, llvm::Triple triple);

  ~TypeSystemClangForExpressions() override = default;

  void Finalize() override;

  UserExpression *
  GetUserExpression(llvm::StringRef expr, llvm::StringRef prefix,
                    lldb::LanguageType language,
                    Expression::ResultType desired_type,
                    const EvaluateExpressionOptions &options,
                    ValueObject *ctx_obj) override;

  FunctionCaller *GetFunctionCaller(const CompilerType &return_type,
                                    const Address &function_address,
                                    const ValueList &arg_value_list,
                                    const char *name) override;

  std::unique_ptr<UtilityFunction>
  CreateUtilityFunction(std::string text, std::string name) override;

  PersistentExpressionState *GetPersistentExpressionState() override;
private:
  lldb::TargetWP m_target_wp;
  std::unique_ptr<ClangPersistentVariables>
      m_persistent_variables; // These are the persistent variables associated
                              // with this process for the expression parser
  std::unique_ptr<ClangASTSource> m_scratch_ast_source_up;
};

} // namespace lldb_private

#endif // LLDB_SOURCE_PLUGINS_TYPESYSTEM_CLANG_TYPESYSTEMCLANG_H
