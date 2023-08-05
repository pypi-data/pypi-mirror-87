//===-- stats.h -------------------------------------------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef SCUDO_STATS_H_
#define SCUDO_STATS_H_

#include "atomic_helpers.h"
#include "list.h"
#include "mutex.h"

#include <string.h>

namespace scudo {

// Memory allocator statistics
enum StatType { StatAllocated, StatFree, StatMapped, StatCount };

typedef uptr StatCounters[StatCount];

// Per-thread stats, live in per-thread cache. We use atomics so that the
// numbers themselves are consistent. But we don't use atomic_{add|sub} or a
// lock, because those are expensive operations , and we only care for the stats
// to be "somewhat" correct: eg. if we call GlobalStats::get while a thread is
// LocalStats::add'ing, this is OK, we will still get a meaningful number.
class LocalStats {
public:
  void initLinkerInitialized() {}
  void init() { memset(this, 0, sizeof(*this)); }

  void add(StatType I, uptr V) {
    V += atomic_load_relaxed(&StatsArray[I]);
    atomic_store_relaxed(&StatsArray[I], V);
  }

  void sub(StatType I, uptr V) {
    V = atomic_load_relaxed(&StatsArray[I]) - V;
    atomic_store_relaxed(&StatsArray[I], V);
  }

  void set(StatType I, uptr V) { atomic_store_relaxed(&StatsArray[I], V); }

  uptr get(StatType I) const { return atomic_load_relaxed(&StatsArray[I]); }

  LocalStats *Next;
  LocalStats *Prev;

private:
  atomic_uptr StatsArray[StatCount];
};

// Global stats, used for aggregation and querying.
class GlobalStats : public LocalStats {
public:
  void initLinkerInitialized() {}
  void init() {
    LocalStats::init();
    Mutex.init();
    StatsList = {};
    initLinkerInitialized();
  }

  void link(LocalStats *S) {
    ScopedLock L(Mutex);
    StatsList.push_back(S);
  }

  void unlink(LocalStats *S) {
    ScopedLock L(Mutex);
    StatsList.remove(S);
    for (uptr I = 0; I < StatCount; I++)
      add(static_cast<StatType>(I), S->get(static_cast<StatType>(I)));
  }

  void get(uptr *S) const {
    ScopedLock L(Mutex);
    for (uptr I = 0; I < StatCount; I++)
      S[I] = LocalStats::get(static_cast<StatType>(I));
    for (const auto &Stats : StatsList) {
      for (uptr I = 0; I < StatCount; I++)
        S[I] += Stats.get(static_cast<StatType>(I));
    }
    // All stats must be non-negative.
    for (uptr I = 0; I < StatCount; I++)
      S[I] = static_cast<sptr>(S[I]) >= 0 ? S[I] : 0;
  }

  void disable() { Mutex.lock(); }
  void enable() { Mutex.unlock(); }

private:
  mutable HybridMutex Mutex;
  DoublyLinkedList<LocalStats> StatsList;
};

} // namespace scudo

#endif // SCUDO_STATS_H_
