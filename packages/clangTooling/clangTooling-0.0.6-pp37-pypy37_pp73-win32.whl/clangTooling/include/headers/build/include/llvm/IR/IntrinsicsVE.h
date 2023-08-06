/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Intrinsic Function Source Fragment                                         *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifndef LLVM_IR_INTRINSIC_VE_ENUMS_H
#define LLVM_IR_INTRINSIC_VE_ENUMS_H

namespace llvm {
namespace Intrinsic {
enum VEIntrinsics : unsigned {
// Enum values for intrinsics
    ve_vl_lsv_vvss = 6861,                            // llvm.ve.vl.lsv.vvss
    ve_vl_lvm_MMss,                            // llvm.ve.vl.lvm.MMss
    ve_vl_lvm_mmss,                            // llvm.ve.vl.lvm.mmss
    ve_vl_lvsd_svs,                            // llvm.ve.vl.lvsd.svs
    ve_vl_lvsl_svs,                            // llvm.ve.vl.lvsl.svs
    ve_vl_lvss_svs,                            // llvm.ve.vl.lvss.svs
    ve_vl_pfchv_ssl,                           // llvm.ve.vl.pfchv.ssl
    ve_vl_pfchvnc_ssl,                         // llvm.ve.vl.pfchvnc.ssl
    ve_vl_pvbrd_vsMvl,                         // llvm.ve.vl.pvbrd.vsMvl
    ve_vl_pvbrd_vsl,                           // llvm.ve.vl.pvbrd.vsl
    ve_vl_pvbrd_vsvl,                          // llvm.ve.vl.pvbrd.vsvl
    ve_vl_svm_sMs,                             // llvm.ve.vl.svm.sMs
    ve_vl_svm_sms,                             // llvm.ve.vl.svm.sms
    ve_vl_vbrdd_vsl,                           // llvm.ve.vl.vbrdd.vsl
    ve_vl_vbrdd_vsmvl,                         // llvm.ve.vl.vbrdd.vsmvl
    ve_vl_vbrdd_vsvl,                          // llvm.ve.vl.vbrdd.vsvl
    ve_vl_vbrdl_vsl,                           // llvm.ve.vl.vbrdl.vsl
    ve_vl_vbrdl_vsmvl,                         // llvm.ve.vl.vbrdl.vsmvl
    ve_vl_vbrdl_vsvl,                          // llvm.ve.vl.vbrdl.vsvl
    ve_vl_vbrds_vsl,                           // llvm.ve.vl.vbrds.vsl
    ve_vl_vbrds_vsmvl,                         // llvm.ve.vl.vbrds.vsmvl
    ve_vl_vbrds_vsvl,                          // llvm.ve.vl.vbrds.vsvl
    ve_vl_vbrdw_vsl,                           // llvm.ve.vl.vbrdw.vsl
    ve_vl_vbrdw_vsmvl,                         // llvm.ve.vl.vbrdw.vsmvl
    ve_vl_vbrdw_vsvl,                          // llvm.ve.vl.vbrdw.vsvl
    ve_vl_vld_vssl,                            // llvm.ve.vl.vld.vssl
    ve_vl_vld_vssvl,                           // llvm.ve.vl.vld.vssvl
    ve_vl_vld2d_vssl,                          // llvm.ve.vl.vld2d.vssl
    ve_vl_vld2d_vssvl,                         // llvm.ve.vl.vld2d.vssvl
    ve_vl_vld2dnc_vssl,                        // llvm.ve.vl.vld2dnc.vssl
    ve_vl_vld2dnc_vssvl,                       // llvm.ve.vl.vld2dnc.vssvl
    ve_vl_vldl2dsx_vssl,                       // llvm.ve.vl.vldl2dsx.vssl
    ve_vl_vldl2dsx_vssvl,                      // llvm.ve.vl.vldl2dsx.vssvl
    ve_vl_vldl2dsxnc_vssl,                     // llvm.ve.vl.vldl2dsxnc.vssl
    ve_vl_vldl2dsxnc_vssvl,                    // llvm.ve.vl.vldl2dsxnc.vssvl
    ve_vl_vldl2dzx_vssl,                       // llvm.ve.vl.vldl2dzx.vssl
    ve_vl_vldl2dzx_vssvl,                      // llvm.ve.vl.vldl2dzx.vssvl
    ve_vl_vldl2dzxnc_vssl,                     // llvm.ve.vl.vldl2dzxnc.vssl
    ve_vl_vldl2dzxnc_vssvl,                    // llvm.ve.vl.vldl2dzxnc.vssvl
    ve_vl_vldlsx_vssl,                         // llvm.ve.vl.vldlsx.vssl
    ve_vl_vldlsx_vssvl,                        // llvm.ve.vl.vldlsx.vssvl
    ve_vl_vldlsxnc_vssl,                       // llvm.ve.vl.vldlsxnc.vssl
    ve_vl_vldlsxnc_vssvl,                      // llvm.ve.vl.vldlsxnc.vssvl
    ve_vl_vldlzx_vssl,                         // llvm.ve.vl.vldlzx.vssl
    ve_vl_vldlzx_vssvl,                        // llvm.ve.vl.vldlzx.vssvl
    ve_vl_vldlzxnc_vssl,                       // llvm.ve.vl.vldlzxnc.vssl
    ve_vl_vldlzxnc_vssvl,                      // llvm.ve.vl.vldlzxnc.vssvl
    ve_vl_vldnc_vssl,                          // llvm.ve.vl.vldnc.vssl
    ve_vl_vldnc_vssvl,                         // llvm.ve.vl.vldnc.vssvl
    ve_vl_vldu_vssl,                           // llvm.ve.vl.vldu.vssl
    ve_vl_vldu_vssvl,                          // llvm.ve.vl.vldu.vssvl
    ve_vl_vldu2d_vssl,                         // llvm.ve.vl.vldu2d.vssl
    ve_vl_vldu2d_vssvl,                        // llvm.ve.vl.vldu2d.vssvl
    ve_vl_vldu2dnc_vssl,                       // llvm.ve.vl.vldu2dnc.vssl
    ve_vl_vldu2dnc_vssvl,                      // llvm.ve.vl.vldu2dnc.vssvl
    ve_vl_vldunc_vssl,                         // llvm.ve.vl.vldunc.vssl
    ve_vl_vldunc_vssvl,                        // llvm.ve.vl.vldunc.vssvl
    ve_vl_vmv_vsvl,                            // llvm.ve.vl.vmv.vsvl
    ve_vl_vmv_vsvmvl,                          // llvm.ve.vl.vmv.vsvmvl
    ve_vl_vmv_vsvvl,                           // llvm.ve.vl.vmv.vsvvl
    ve_vl_vst_vssl,                            // llvm.ve.vl.vst.vssl
    ve_vl_vst_vssml,                           // llvm.ve.vl.vst.vssml
    ve_vl_vst2d_vssl,                          // llvm.ve.vl.vst2d.vssl
    ve_vl_vst2d_vssml,                         // llvm.ve.vl.vst2d.vssml
    ve_vl_vst2dnc_vssl,                        // llvm.ve.vl.vst2dnc.vssl
    ve_vl_vst2dnc_vssml,                       // llvm.ve.vl.vst2dnc.vssml
    ve_vl_vst2dncot_vssl,                      // llvm.ve.vl.vst2dncot.vssl
    ve_vl_vst2dncot_vssml,                     // llvm.ve.vl.vst2dncot.vssml
    ve_vl_vst2dot_vssl,                        // llvm.ve.vl.vst2dot.vssl
    ve_vl_vst2dot_vssml,                       // llvm.ve.vl.vst2dot.vssml
    ve_vl_vstl_vssl,                           // llvm.ve.vl.vstl.vssl
    ve_vl_vstl_vssml,                          // llvm.ve.vl.vstl.vssml
    ve_vl_vstl2d_vssl,                         // llvm.ve.vl.vstl2d.vssl
    ve_vl_vstl2d_vssml,                        // llvm.ve.vl.vstl2d.vssml
    ve_vl_vstl2dnc_vssl,                       // llvm.ve.vl.vstl2dnc.vssl
    ve_vl_vstl2dnc_vssml,                      // llvm.ve.vl.vstl2dnc.vssml
    ve_vl_vstl2dncot_vssl,                     // llvm.ve.vl.vstl2dncot.vssl
    ve_vl_vstl2dncot_vssml,                    // llvm.ve.vl.vstl2dncot.vssml
    ve_vl_vstl2dot_vssl,                       // llvm.ve.vl.vstl2dot.vssl
    ve_vl_vstl2dot_vssml,                      // llvm.ve.vl.vstl2dot.vssml
    ve_vl_vstlnc_vssl,                         // llvm.ve.vl.vstlnc.vssl
    ve_vl_vstlnc_vssml,                        // llvm.ve.vl.vstlnc.vssml
    ve_vl_vstlncot_vssl,                       // llvm.ve.vl.vstlncot.vssl
    ve_vl_vstlncot_vssml,                      // llvm.ve.vl.vstlncot.vssml
    ve_vl_vstlot_vssl,                         // llvm.ve.vl.vstlot.vssl
    ve_vl_vstlot_vssml,                        // llvm.ve.vl.vstlot.vssml
    ve_vl_vstnc_vssl,                          // llvm.ve.vl.vstnc.vssl
    ve_vl_vstnc_vssml,                         // llvm.ve.vl.vstnc.vssml
    ve_vl_vstncot_vssl,                        // llvm.ve.vl.vstncot.vssl
    ve_vl_vstncot_vssml,                       // llvm.ve.vl.vstncot.vssml
    ve_vl_vstot_vssl,                          // llvm.ve.vl.vstot.vssl
    ve_vl_vstot_vssml,                         // llvm.ve.vl.vstot.vssml
    ve_vl_vstu_vssl,                           // llvm.ve.vl.vstu.vssl
    ve_vl_vstu_vssml,                          // llvm.ve.vl.vstu.vssml
    ve_vl_vstu2d_vssl,                         // llvm.ve.vl.vstu2d.vssl
    ve_vl_vstu2d_vssml,                        // llvm.ve.vl.vstu2d.vssml
    ve_vl_vstu2dnc_vssl,                       // llvm.ve.vl.vstu2dnc.vssl
    ve_vl_vstu2dnc_vssml,                      // llvm.ve.vl.vstu2dnc.vssml
    ve_vl_vstu2dncot_vssl,                     // llvm.ve.vl.vstu2dncot.vssl
    ve_vl_vstu2dncot_vssml,                    // llvm.ve.vl.vstu2dncot.vssml
    ve_vl_vstu2dot_vssl,                       // llvm.ve.vl.vstu2dot.vssl
    ve_vl_vstu2dot_vssml,                      // llvm.ve.vl.vstu2dot.vssml
    ve_vl_vstunc_vssl,                         // llvm.ve.vl.vstunc.vssl
    ve_vl_vstunc_vssml,                        // llvm.ve.vl.vstunc.vssml
    ve_vl_vstuncot_vssl,                       // llvm.ve.vl.vstuncot.vssl
    ve_vl_vstuncot_vssml,                      // llvm.ve.vl.vstuncot.vssml
    ve_vl_vstuot_vssl,                         // llvm.ve.vl.vstuot.vssl
    ve_vl_vstuot_vssml,                        // llvm.ve.vl.vstuot.vssml
}; // enum
} // namespace Intrinsic
} // namespace llvm

#endif
