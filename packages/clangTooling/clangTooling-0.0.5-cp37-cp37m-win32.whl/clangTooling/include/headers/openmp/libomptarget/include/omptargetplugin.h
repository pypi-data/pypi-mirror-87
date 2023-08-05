//===-- omptargetplugin.h - Target dependent OpenMP Plugin API --*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//
//
// This file defines an interface between target independent OpenMP offload
// runtime library libomptarget and target dependent plugin.
//
//===----------------------------------------------------------------------===//

#ifndef _OMPTARGETPLUGIN_H_
#define _OMPTARGETPLUGIN_H_

#include <omptarget.h>

#ifdef __cplusplus
extern "C" {
#endif

// Return the number of available devices of the type supported by the
// target RTL.
int32_t __tgt_rtl_number_of_devices(void);

// Return an integer different from zero if the provided device image can be
// supported by the runtime. The functionality is similar to comparing the
// result of __tgt__rtl__load__binary to NULL. However, this is meant to be a
// lightweight query to determine if the RTL is suitable for an image without
// having to load the library, which can be expensive.
int32_t __tgt_rtl_is_valid_binary(__tgt_device_image *Image);

// Return an integer other than zero if the data can be exchaned from SrcDevId
// to DstDevId. If it is data exchangable, the device plugin should provide
// function to move data from source device to destination device directly.
int32_t __tgt_rtl_is_data_exchangable(int32_t SrcDevId, int32_t DstDevId);

// Initialize the requires flags for the device.
int64_t __tgt_rtl_init_requires(int64_t RequiresFlags);

// Initialize the specified device. In case of success return 0; otherwise
// return an error code.
int32_t __tgt_rtl_init_device(int32_t ID);

// Pass an executable image section described by image to the specified
// device and prepare an address table of target entities. In case of error,
// return NULL. Otherwise, return a pointer to the built address table.
// Individual entries in the table may also be NULL, when the corresponding
// offload region is not supported on the target device.
__tgt_target_table *__tgt_rtl_load_binary(int32_t ID,
                                          __tgt_device_image *Image);

// Allocate data on the particular target device, of the specified size.
// HostPtr is a address of the host data the allocated target data
// will be associated with (HostPtr may be NULL if it is not known at
// allocation time, like for example it would be for target data that
// is allocated by omp_target_alloc() API). Return address of the
// allocated data on the target that will be used by libomptarget.so to
// initialize the target data mapping structures. These addresses are
// used to generate a table of target variables to pass to
// __tgt_rtl_run_region(). The __tgt_rtl_data_alloc() returns NULL in
// case an error occurred on the target device.
void *__tgt_rtl_data_alloc(int32_t ID, int64_t Size, void *HostPtr);

// Pass the data content to the target device using the target address. In case
// of success, return zero. Otherwise, return an error code.
int32_t __tgt_rtl_data_submit(int32_t ID, void *TargetPtr, void *HostPtr,
                              int64_t Size);

int32_t __tgt_rtl_data_submit_async(int32_t ID, void *TargetPtr, void *HostPtr,
                                    int64_t Size,
                                    __tgt_async_info *AsyncInfoPtr);

// Retrieve the data content from the target device using its address. In case
// of success, return zero. Otherwise, return an error code.
int32_t __tgt_rtl_data_retrieve(int32_t ID, void *HostPtr, void *TargetPtr,
                                int64_t Size);

// Asynchronous version of __tgt_rtl_data_retrieve
int32_t __tgt_rtl_data_retrieve_async(int32_t ID, void *HostPtr,
                                      void *TargetPtr, int64_t Size,
                                      __tgt_async_info *AsyncInfoPtr);

// Copy the data content from one target device to another target device using
// its address. This operation does not need to copy data back to host and then
// from host to another device. In case of success, return zero. Otherwise,
// return an error code.
int32_t __tgt_rtl_data_exchange(int32_t SrcID, void *SrcPtr, int32_t DstID,
                                void *DstPtr, int64_t Size);

// Asynchronous version of __tgt_rtl_data_exchange
int32_t __tgt_rtl_data_exchange_async(int32_t SrcID, void *SrcPtr,
                                      int32_t DesID, void *DstPtr, int64_t Size,
                                      __tgt_async_info *AsyncInfoPtr);

// De-allocate the data referenced by target ptr on the device. In case of
// success, return zero. Otherwise, return an error code.
int32_t __tgt_rtl_data_delete(int32_t ID, void *TargetPtr);

// Transfer control to the offloaded entry Entry on the target device.
// Args and Offsets are arrays of NumArgs size of target addresses and
// offsets. An offset should be added to the target address before passing it
// to the outlined function on device side. If AsyncInfoPtr is nullptr, it is
// synchronous; otherwise it is asynchronous. However, AsyncInfoPtr may be
// ignored on some platforms, like x86_64. In that case, it is synchronous. In
// case of success, return zero. Otherwise, return an error code.
int32_t __tgt_rtl_run_target_region(int32_t ID, void *Entry, void **Args,
                                    ptrdiff_t *Offsets, int32_t NumArgs);

// Asynchronous version of __tgt_rtl_run_target_region
int32_t __tgt_rtl_run_target_region_async(int32_t ID, void *Entry, void **Args,
                                          ptrdiff_t *Offsets, int32_t NumArgs,
                                          __tgt_async_info *AsyncInfoPtr);

// Similar to __tgt_rtl_run_target_region, but additionally specify the
// number of teams to be created and a number of threads in each team. If
// AsyncInfoPtr is nullptr, it is synchronous; otherwise it is asynchronous.
// However, AsyncInfoPtr may be ignored on some platforms, like x86_64. In that
// case, it is synchronous.
int32_t __tgt_rtl_run_target_team_region(int32_t ID, void *Entry, void **Args,
                                         ptrdiff_t *Offsets, int32_t NumArgs,
                                         int32_t NumTeams, int32_t ThreadLimit,
                                         uint64_t loop_tripcount);

// Asynchronous version of __tgt_rtl_run_target_team_region
int32_t __tgt_rtl_run_target_team_region_async(
    int32_t ID, void *Entry, void **Args, ptrdiff_t *Offsets, int32_t NumArgs,
    int32_t NumTeams, int32_t ThreadLimit, uint64_t loop_tripcount,
    __tgt_async_info *AsyncInfoPtr);

// Device synchronization. In case of success, return zero. Otherwise, return an
// error code.
int32_t __tgt_rtl_synchronize(int32_t ID, __tgt_async_info *AsyncInfoPtr);

#ifdef __cplusplus
}
#endif

#endif // _OMPTARGETPLUGIN_H_
