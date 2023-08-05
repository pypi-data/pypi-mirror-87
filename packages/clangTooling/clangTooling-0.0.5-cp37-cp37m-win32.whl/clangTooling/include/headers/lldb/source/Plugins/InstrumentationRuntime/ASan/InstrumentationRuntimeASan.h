//===-- InstrumentationRuntimeASan.h ----------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef LLDB_SOURCE_PLUGINS_INSTRUMENTATIONRUNTIME_ASAN_INSTRUMENTATIONRUNTIMEASAN_H
#define LLDB_SOURCE_PLUGINS_INSTRUMENTATIONRUNTIME_ASAN_INSTRUMENTATIONRUNTIMEASAN_H

#include "lldb/Target/InstrumentationRuntime.h"
#include "lldb/Target/Process.h"
#include "lldb/Utility/StructuredData.h"
#include "lldb/lldb-private.h"

namespace lldb_private {

class InstrumentationRuntimeASan : public lldb_private::InstrumentationRuntime {
public:
  ~InstrumentationRuntimeASan() override;

  static lldb::InstrumentationRuntimeSP
  CreateInstance(const lldb::ProcessSP &process_sp);

  static void Initialize();

  static void Terminate();

  static lldb_private::ConstString GetPluginNameStatic();

  static lldb::InstrumentationRuntimeType GetTypeStatic();

  lldb_private::ConstString GetPluginName() override {
    return GetPluginNameStatic();
  }

  virtual lldb::InstrumentationRuntimeType GetType() { return GetTypeStatic(); }

  uint32_t GetPluginVersion() override { return 1; }

private:
  InstrumentationRuntimeASan(const lldb::ProcessSP &process_sp)
      : lldb_private::InstrumentationRuntime(process_sp) {}

  const RegularExpression &GetPatternForRuntimeLibrary() override;

  bool CheckIfRuntimeIsValid(const lldb::ModuleSP module_sp) override;

  void Activate() override;

  void Deactivate();

  static bool NotifyBreakpointHit(void *baton,
                                  StoppointCallbackContext *context,
                                  lldb::user_id_t break_id,
                                  lldb::user_id_t break_loc_id);

  StructuredData::ObjectSP RetrieveReportData();

  std::string FormatDescription(StructuredData::ObjectSP report);
};

} // namespace lldb_private

#endif // LLDB_SOURCE_PLUGINS_INSTRUMENTATIONRUNTIME_ASAN_INSTRUMENTATIONRUNTIMEASAN_H
