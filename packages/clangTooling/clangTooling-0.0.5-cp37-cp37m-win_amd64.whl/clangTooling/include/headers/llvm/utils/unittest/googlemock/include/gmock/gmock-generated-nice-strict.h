// This file was GENERATED by command:
//     pump.py gmock-generated-nice-strict.h.pump
// DO NOT EDIT BY HAND!!!

// Copyright 2008, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// Author: wan@google.com (Zhanyong Wan)

// Implements class templates NiceMock, NaggyMock, and StrictMock.
//
// Given a mock class MockFoo that is created using Google Mock,
// NiceMock<MockFoo> is a subclass of MockFoo that allows
// uninteresting calls (i.e. calls to mock methods that have no
// EXPECT_CALL specs), NaggyMock<MockFoo> is a subclass of MockFoo
// that prints a warning when an uninteresting call occurs, and
// StrictMock<MockFoo> is a subclass of MockFoo that treats all
// uninteresting calls as errors.
//
// Currently a mock is naggy by default, so MockFoo and
// NaggyMock<MockFoo> behave like the same.  However, we will soon
// switch the default behavior of mocks to be nice, as that in general
// leads to more maintainable tests.  When that happens, MockFoo will
// stop behaving like NaggyMock<MockFoo> and start behaving like
// NiceMock<MockFoo>.
//
// NiceMock, NaggyMock, and StrictMock "inherit" the constructors of
// their respective base class, with up-to 10 arguments.  Therefore
// you can write NiceMock<MockFoo>(5, "a") to construct a nice mock
// where MockFoo has a constructor that accepts (int, const char*),
// for example.
//
// A known limitation is that NiceMock<MockFoo>, NaggyMock<MockFoo>,
// and StrictMock<MockFoo> only works for mock methods defined using
// the MOCK_METHOD* family of macros DIRECTLY in the MockFoo class.
// If a mock method is defined in a base class of MockFoo, the "nice"
// or "strict" modifier may not affect it, depending on the compiler.
// In particular, nesting NiceMock, NaggyMock, and StrictMock is NOT
// supported.
//
// Another known limitation is that the constructors of the base mock
// cannot have arguments passed by non-const reference, which are
// banned by the Google C++ style guide anyway.

// IWYU pragma: private, include "gmock/gmock.h"

#ifndef GMOCK_INCLUDE_GMOCK_GMOCK_GENERATED_NICE_STRICT_H_
#define GMOCK_INCLUDE_GMOCK_GMOCK_GENERATED_NICE_STRICT_H_

#include "gmock/gmock-spec-builders.h"
#include "gmock/internal/gmock-port.h"

namespace testing {

template <class MockClass>
class NiceMock : public MockClass {
 public:
  // We don't factor out the constructor body to a common method, as
  // we have to avoid a possible clash with members of MockClass.
  NiceMock() {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  // C++ doesn't (yet) allow inheritance of constructors, so we have
  // to define it for each arity.
  template <typename A1>
  explicit NiceMock(const A1& a1) : MockClass(a1) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }
  template <typename A1, typename A2>
  NiceMock(const A1& a1, const A2& a2) : MockClass(a1, a2) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3>
  NiceMock(const A1& a1, const A2& a2, const A3& a3) : MockClass(a1, a2, a3) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4>
  NiceMock(const A1& a1, const A2& a2, const A3& a3,
      const A4& a4) : MockClass(a1, a2, a3, a4) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5) : MockClass(a1, a2, a3, a4, a5) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6) : MockClass(a1, a2, a3, a4, a5, a6) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7) : MockClass(a1, a2, a3, a4, a5,
      a6, a7) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8) : MockClass(a1,
      a2, a3, a4, a5, a6, a7, a8) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8,
      const A9& a9) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9, typename A10>
  NiceMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8, const A9& a9,
      const A10& a10) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10) {
    ::testing::Mock::AllowUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  virtual ~NiceMock() {
    ::testing::Mock::UnregisterCallReaction(
        internal::ImplicitCast_<MockClass*>(this));
  }

 private:
  GTEST_DISALLOW_COPY_AND_ASSIGN_(NiceMock);
};

template <class MockClass>
class NaggyMock : public MockClass {
 public:
  // We don't factor out the constructor body to a common method, as
  // we have to avoid a possible clash with members of MockClass.
  NaggyMock() {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  // C++ doesn't (yet) allow inheritance of constructors, so we have
  // to define it for each arity.
  template <typename A1>
  explicit NaggyMock(const A1& a1) : MockClass(a1) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }
  template <typename A1, typename A2>
  NaggyMock(const A1& a1, const A2& a2) : MockClass(a1, a2) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3) : MockClass(a1, a2, a3) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3,
      const A4& a4) : MockClass(a1, a2, a3, a4) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5) : MockClass(a1, a2, a3, a4, a5) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6) : MockClass(a1, a2, a3, a4, a5, a6) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7) : MockClass(a1, a2, a3, a4, a5,
      a6, a7) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8) : MockClass(a1,
      a2, a3, a4, a5, a6, a7, a8) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8,
      const A9& a9) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9, typename A10>
  NaggyMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8, const A9& a9,
      const A10& a10) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10) {
    ::testing::Mock::WarnUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  virtual ~NaggyMock() {
    ::testing::Mock::UnregisterCallReaction(
        internal::ImplicitCast_<MockClass*>(this));
  }

 private:
  GTEST_DISALLOW_COPY_AND_ASSIGN_(NaggyMock);
};

template <class MockClass>
class StrictMock : public MockClass {
 public:
  // We don't factor out the constructor body to a common method, as
  // we have to avoid a possible clash with members of MockClass.
  StrictMock() {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  // C++ doesn't (yet) allow inheritance of constructors, so we have
  // to define it for each arity.
  template <typename A1>
  explicit StrictMock(const A1& a1) : MockClass(a1) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }
  template <typename A1, typename A2>
  StrictMock(const A1& a1, const A2& a2) : MockClass(a1, a2) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3>
  StrictMock(const A1& a1, const A2& a2, const A3& a3) : MockClass(a1, a2, a3) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4>
  StrictMock(const A1& a1, const A2& a2, const A3& a3,
      const A4& a4) : MockClass(a1, a2, a3, a4) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5) : MockClass(a1, a2, a3, a4, a5) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6) : MockClass(a1, a2, a3, a4, a5, a6) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7) : MockClass(a1, a2, a3, a4, a5,
      a6, a7) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8) : MockClass(a1,
      a2, a3, a4, a5, a6, a7, a8) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8,
      const A9& a9) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  template <typename A1, typename A2, typename A3, typename A4, typename A5,
      typename A6, typename A7, typename A8, typename A9, typename A10>
  StrictMock(const A1& a1, const A2& a2, const A3& a3, const A4& a4,
      const A5& a5, const A6& a6, const A7& a7, const A8& a8, const A9& a9,
      const A10& a10) : MockClass(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10) {
    ::testing::Mock::FailUninterestingCalls(
        internal::ImplicitCast_<MockClass*>(this));
  }

  virtual ~StrictMock() {
    ::testing::Mock::UnregisterCallReaction(
        internal::ImplicitCast_<MockClass*>(this));
  }

 private:
  GTEST_DISALLOW_COPY_AND_ASSIGN_(StrictMock);
};

// The following specializations catch some (relatively more common)
// user errors of nesting nice and strict mocks.  They do NOT catch
// all possible errors.

// These specializations are declared but not defined, as NiceMock,
// NaggyMock, and StrictMock cannot be nested.

template <typename MockClass>
class NiceMock<NiceMock<MockClass> >;
template <typename MockClass>
class NiceMock<NaggyMock<MockClass> >;
template <typename MockClass>
class NiceMock<StrictMock<MockClass> >;

template <typename MockClass>
class NaggyMock<NiceMock<MockClass> >;
template <typename MockClass>
class NaggyMock<NaggyMock<MockClass> >;
template <typename MockClass>
class NaggyMock<StrictMock<MockClass> >;

template <typename MockClass>
class StrictMock<NiceMock<MockClass> >;
template <typename MockClass>
class StrictMock<NaggyMock<MockClass> >;
template <typename MockClass>
class StrictMock<StrictMock<MockClass> >;

}  // namespace testing

#endif  // GMOCK_INCLUDE_GMOCK_GMOCK_GENERATED_NICE_STRICT_H_
