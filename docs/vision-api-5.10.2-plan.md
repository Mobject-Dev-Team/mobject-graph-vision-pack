# TwinCAT Vision 5.10.2 coverage and implementation plan

Initially reviewed 8 September 2026 against repository commit `e46b70f` and the supplied Tc3 Vision API 5.10.2.0 export, dated 26 June 2026. The export is a local reference named `Tc3_Vision_Api_5.10.2.html`; it is deliberately ignored by Git and must never be committed or pushed.

The initial scope was **225 new function nodes, completion of one disabled function node, 15 new named value datatype wrappers, and updates to existing wrappers**. There is also a substantial interface and stateful function-block backlog. Implement the foundations and repairs first, then deliver related node families in buildable batches.

These are gaps between this project and the supplied API, **not a list of features introduced in 5.10.2**. The older complete API export is not present, and the library's wildcard reference does not prove which Vision PLC library was last used to compile it.

## Implementation progress — first batch

The following source changes are implemented; TwinCAT compilation and runtime acceptance remain pending:

- Added and registered all 15 named value datatype wrappers, including documented ROI/Walsh defaults, nested member references, and clones that copy the active value.
- Added the 42 missing enum values. Corrected the Huber enum and BRISK member labels while retaining deserialization of their legacy names.
- Exposed the triangle `fArea` output. A skipped or failed call preserves the last successful area.
- Added `Node_F_VN_SalientFeatures`, `Node_F_VN_FindRois`, and `Node_F_VN_MergeRegions` under `Vision/Image Analysis/Object Detection`, including ports, parameters, cloning, and pre-execution checks.
- Set the Vision default resolution to `5.10.2.0` in both PLC projects. Aligned the test project with core `0.10.0`, graph `0.18.0`, and vision pack `0.11.0`.
- Added two TcUnit suites covering datatype discovery, serialization and legacy names, numeric widths, nested references, defaults, clone independence, triangle area/failure chaining, region merging, and salient-feature/ROI processing.
- Added a repository ignore rule for the local HTML export and `--api PATH` support in the audit tool. Removing the local reference does not remove the saved inventories or affect the PLC sources.

The first batch reached 873 registered nodes, including 816 API function nodes, and 185 registered datatypes. All 162 exported named value types have source wrappers; 161 are registered and `_TcVnMatrix` remains disabled. Interface and stateful-function-block work remains as listed below.

Before running the new tests on Windows, install Vision `5.10.2.0`, build and install the modified `0.11.0` library, then rebuild the test PLC. An older installed `0.11.0` binary is not sufficient. Refresh the test project's `5.8.4.0` runtime repository through TwinCAT, confirm the resolved library/runtime versions, and run both new suites along with the existing suites. The root `.library` and checked-in runtime binaries have not been regenerated in this Linux workspace.

## Implementation progress — second batch

Added eight function nodes with compile entries, factory registrations, cloning, documented expert defaults, and pre-execution checks:

| Graph category under `Vision` | Added API functions |
| --- | --- |
| Image Color and Contrast Processing | `F_VN_InvertImageColorExp`, `F_VN_NormalizeImageExp` |
| Image Analysis/Object Detection | `F_VN_MatchTemplateExp`, `F_VN_MatchTemplateAndEvaluateExp` |
| Keypoint Features | `F_VN_MatchDescriptorsBFExp`, `F_VN_MatchDescriptorsKnnBFExp` |
| Contour Analysis | `F_VN_MatchContours`, `F_VN_MatchContoursExp` |

Optional masks are exposed as image inputs and accept an unconnected value. Template evaluation exposes both matching positions and scores; its threshold is restricted to 0–1 only for normalized methods. Template checks distinguish USINT/REAL element types and check template/mask dimensions and formats. Descriptor nodes check matching descriptor formats and lengths, supported norms, and positive `nK`; KNN starts at 2 neighbors. Contour matching exposes scalar dissimilarity and the expert weighting factors.

Extended the registered node TcUnit suite with four tests covering all eight nodes: custom 12-bit inversion and failure chaining; normalization range, destination type, and mask behavior; template result dimensions/scores and invalid threshold/scale/mask checks; descriptor self-matches and ordered neighbors; and contour translation invariance versus weighted position differences. These tests are authored but **not executed** here. The matching fixtures require the TC3 Vision Matching licence, in addition to the Base licence used by the image fixtures.

Current source coverage is **881 registered nodes**, including **824 API function nodes**, and **185 registered datatypes**. There are **214 missing function nodes** plus the disabled matrix-multiplication node. Structural inventory checks report no existing-wrapper argument or enum/member-label gaps. The generated audit files reflect this batch; the initial table below remains the baseline.

`CustomFilter`, `CustomFilterExp`, `SeparableCustomFilter`, and `SeparableCustomFilterExp` require `TcVnMatrix`. Their implementation is deferred until phase 2 provides a usable matrix wrapper and buffer lifetime handling. Other ordinary function batches using registered datatypes can proceed independently. TwinCAT build, TcUnit execution, and runtime validation remain required for both completed source batches.

## About box release notes

Copy this entry into the About box release-notes array. It lists the 11 new nodes implemented across both batches. Keep this entry updated as further nodes are implemented. `v1.26.0 beta` is a proposed version following the supplied `v1.25.0 beta` example; adjust the version and date to match the eventual release. This is a draft while TwinCAT build and runtime validation remain pending.

```javascript
{
  version: "v1.26.0 beta",
  date: "8th September 2026",
  nodes: [
    {
      name: "F_VN_SalientFeatures",
      description: "Extract salient image features for region detection.",
    },
    {
      name: "F_VN_FindRois",
      description: "Find regions of interest in a feature image.",
    },
    {
      name: "F_VN_MergeRegions",
      description: "Merge overlapping or nearby rectangular regions.",
    },
    {
      name: "F_VN_InvertImageColorExp",
      description: "Invert image colors with a configurable maximum pixel value.",
    },
    {
      name: "F_VN_NormalizeImageExp",
      description: "Normalize image values with configurable range, output type, and optional mask.",
    },
    {
      name: "F_VN_MatchTemplateExp",
      description: "Match a template image using a selectable comparison method and optional mask.",
    },
    {
      name: "F_VN_MatchTemplateAndEvaluateExp",
      description: "Find template matches and return their positions and scores, with optional masking and scaling.",
    },
    {
      name: "F_VN_MatchDescriptorsBFExp",
      description: "Match descriptors using brute force with selectable distance norm, optional mask, and cross-checking.",
    },
    {
      name: "F_VN_MatchDescriptorsKnnBFExp",
      description: "Find the nearest descriptor matches with configurable neighbor count, distance norm, and optional mask.",
    },
    {
      name: "F_VN_MatchContours",
      description: "Compare contours using Hu moment invariants and return their dissimilarity.",
    },
    {
      name: "F_VN_MatchContoursExp",
      description: "Compare contours with additional weighting for area, position, and contour-count differences.",
    },
  ],
},
```

## Initial coverage and complete inventories

“Registered” means that the source exists, is enabled in the library `.plcproj`, and is registered in `VisionNodePack` or `VisionDatatypePack`. It does not certify runtime correctness or compatibility with an installed 5.10.2 runtime.

| API surface | API entries | Registered | Existing but unavailable | No wrapper source |
| --- | ---: | ---: | ---: | ---: |
| `F_VN_*` functions | 1,039 | 813 | 1 excluded | 225 |
| Aliases | 9 | 8 | 0 | 1 |
| Named arrays | 29 | 29 | 0 | 0 |
| Enums | 92 | 82 | 0 | 10 |
| Structs | 32 | 27 | 1 excluded | 4 |
| Interfaces | 113 | 3 | 1 unregistered | 109 |
| Constants, exposed as nodes | 47 | 47 | 0 | 0 |
| `FB_VN_*` function blocks | 25 | 0 | 1 excluded | 24 |

The initial project had 870 registered nodes overall and 170 registered datatypes. Those totals also include graph helpers, colour constants, and backing array wrappers that are not separate entries in the API inventory. Do not add these totals to the API counts above.

The accompanying files identify every symbol; they are the implementation checklist:

- [All remaining missing function nodes](vision-api-5.10.2-audit/missing-function-nodes.md), grouped by the export's required licence.
- [All 1,039 functions](vision-api-5.10.2-audit/functions.csv): status, proposed node name, existing graph path, signature, defaults, required types, missing types mentioned in parameter comments, pointer parameters, and existing helper call sites.
- [All datatypes and constants](vision-api-5.10.2-audit/datatypes-and-constants.csv), plus [every enum value and struct member](vision-api-5.10.2-audit/datatype-members.csv).
- [All interfaces](vision-api-5.10.2-audit/interfaces.csv): wrapper status, scope, inheritance description, and declared method signatures. Inherited methods belong to the base-interface entry.
- [All function blocks](vision-api-5.10.2-audit/function-blocks.csv): status, cyclic input/output parameters, or method signatures for blocks exposing methods.
- [Existing wrapper gaps](vision-api-5.10.2-audit/existing-wrapper-gaps.csv), [project registration](vision-api-5.10.2-audit/project-registration.csv), and [count summary](vision-api-5.10.2-audit/summary.json).

Regenerate these inventories with `python3 tools/audit_vision_api.py` while the ignored local export is present, or `python3 tools/audit_vision_api.py --api /path/to/Tc3_Vision_Api_5.10.2.html`. The script uses Python's standard library and only writes the audit directory. It reports a clear error if the local export has been removed; the saved inventories remain readable. The plan itself is maintained separately. Keep the generated CSV files together so source absence, build exclusion, and missing registration remain distinguishable.

## Establish the version and test baseline first

At the initial audit, the [library project](../src/sln/lib/mobject-graph-vision-pack/mobject-graph-vision-pack.plcproj) declared:

- Project version `0.11.0`; TwinCAT `ProgramVersion` `3.1.4026.25`.
- `mobject-core` `0.10.0`, `mobject-graph` `0.18.0`, and `mobject-graph-plc-pack` `0.19.0`.
- `Tc3_Vision, *` as a placeholder reference.

The [test PLC project](../src/sln/libTest/Main/Main.plcproj) initially referenced `mobject-core` `0.9.0` and the installed `mobject-graph-vision-pack` `0.10.0`; these references are now aligned as described above. Its checked-in [Vision header](<../src/sln/libTest/_Repository/Beckhoff Automation GmbH/Tc3_Vision/5.8.4.0/Tc3_Vision.h>) and runtime modules remain version `5.8.4.0`. These files establish the checked-in dependency state, not the version installed on a developer's machine.

Before implementing new nodes:

1. Establish a Windows TwinCAT build environment with the supplied API's `Tc3_Vision` `5.10.2.0` PLC library and corresponding runtime components. Verify the required TwinCAT build and runtime licences there; the HTML is a reference export, not an installable library.
2. Record or pin the intended Vision resolution so builds do not silently select a different API. Decide the minimum supported Vision version for the next release. Recommend targeting 5.10.2 for this coverage work; supporting older versions needs a separate compatibility build.
3. Update the test project's references to match the library under development and ensure the test PLC actually loads the newly built library. Align `mobject-core`, and refresh the checked-in runtime dependencies using TwinCAT tooling.
4. Build the existing solution and run the existing TcUnit suites before making PLC changes. [MAIN](../src/sln/libTest/Main/POUs/MAIN.TcPOU) instantiates ten suites: seven enum suites, two interface suites, and one struct suite. There are no node-specific test suites in the checked-in test directory.

Acceptance: both PLC projects build against the recorded versions, the test PLC demonstrably uses the development library, and baseline test results are recorded. The older test dependency must not be used to claim validation of new nodes.

## Repair existing coverage

These repairs are additional to the missing-source counts.

| Existing implementation | Finding | Work required |
| --- | --- | --- |
| `Node_F_VN_MultiplyMatrices` and `_TcVnMatrix` | Both exist, are excluded from compilation, and are absent from pack registration. | Finish matrix buffer handling, validate shape and element type, enable both, and register them. Coordinate with the missing `F_VN_InitMatrixStruct` node. |
| `Node_FB_VN_InitializeFunction` | Exists but is excluded and unregistered. `OnExecute` hardcodes `TCVN_IF_OCR` despite exposing `eFunction`; it omits timeout and busy/error outputs and collapses errors to `-1`. | Use `eFunction.Value`, expose `nTimeout`, `bBusy`, `bError`, and `nErrorId`, preserve useful failure information, and define execution across PLC cycles before enabling it. |
| `_ITcVnBidirectionalIterator` | Compiled but not registered. | Review its copy/reference/release behavior and register it with the iterator family. |
| `Node_F_VN_EnclosingTriangle` | Omits the API's `fArea : LREAL` output from the call and graph ports. | Add an output wrapper, capture `fArea =>` through an appropriate local value, and publish the result. |
| `_ETcVnDistanceType` | Registers the label `TCVN_DT_HUBER ` with a trailing space. | Correct the label, considering compatibility with saved enum values. |
| `_TcVnParamsBRISK` | Registers the member label `fPatternScale ` with a trailing space. | Correct the member name, considering compatibility with saved structured values. |

Add **42 enum values across six existing wrappers**:

| Wrapper | Missing values |
| --- | --- |
| `_ETcVnColorSpaceTransform` | 28 RGB/BGR/RGBA/BGRA to YUV 4:2:2 entries. The complete names are in `existing-wrapper-gaps.csv`. |
| `_ETcVnInterpolationType` | `TCVN_IT_BILINEAR_EXACT`, `TCVN_IT_NEAREST_NEIGHBOR_EXACT` |
| `_ETcVnOcrModelType` | `TCVN_OMT_CNN_NUMBERS_SC_LETTERS` |
| `_ETcVnOcrOptions` | `TCVN_OO_NONE`, `TCVN_OO_NOVELTY_LEVEL1`, `TCVN_OO_NOVELTY_LEVEL2`, `TCVN_OO_NOVELTY_LEVEL3` |
| `_ETcVnPixelPackMode` | `TCVN_PPM_MONO14P` |
| `_ETcVnTimestamp` | `TCVN_TS_CAMERA`, `TCVN_TS_CUSTOM`, `TCVN_TS_GETCURRENTIMAGE`, `TCVN_TS_LAST_CHANGE`, `TCVN_TS_RECEPTION_FINISHED`, `TCVN_TS_RECEPTION_STARTED` |

Seven backing arrays also exist and compile but are not registered directly: `_Array0to2OfTcVnPoint2_REAL`, `_Array0to32OfUDINT`, `_Array0to3OfSINT`, `_Array0to3OfTcVnPoint2_REAL`, `_Array0to3OfUINT`, `_Array0to3OfUSINT`, and `_Array0to9OfITcVnImage`. Their named Vision aliases **are registered**. Check whether standalone backing-array construction/deserialization needs direct registration; this is not seven missing named Vision arrays. Register them if that is the graph datatype pack's intended convention and add the corresponding construction test.

`_ALIASTYP` and `_Array0to1OfARRAYTYP` are excluded templates. Keep them excluded; they are not missing API implementations.

## Create the 15 missing named value datatype wrappers

Use `_TypeName` wrappers around the native `Tc3_Vision` type; do not redefine Beckhoff's types. Each needs a `.TcPOU`, a project compile entry, and a declaration and registration in `VisionDatatypePack`. Use existing alias, enum, and structured datatype patterns for references, cloning, and member access.

| New wrapper | Native base or prerequisite | Purpose / dependent work |
| --- | --- | --- |
| `_GVCP_REGISTER_VALUE` | `UDINT` | Register values and the address/value pair below. |
| `_ETcVnComparisonOperator` | `INT` | `SortContainer` and `SortContainerExp`. |
| `_ETcVnDetectBarcodesWalshOptions` | `UDINT` | Walsh barcode detection options. |
| `_ETcVnDetectPatternPointsOptions` | `UDINT` | `DetectPatternPoints2` flags. |
| `_ETcVnDotCodeOptions` | `ULINT` | Named options for existing DotCode reading nodes. |
| `_ETcVnEdgeSelection` | `DINT` | Axis-aligned edge location. |
| `_ETcVnFindRoisMethod` | `UDINT` | ROI finding. |
| `_ETcVnJpegSampling` | `DINT` | JPEG export options. |
| `_ETcVnMergeRegionsOptions` | `ULINT` | Region merging flags. |
| `_ETcVnPolarizedImageInterpolation` | `DINT` | Polarized-image demosaicing. |
| `_ETcVnSalientFeaturesMethod` | `UDINT` | Salient feature extraction. |
| `_GVCP_ADDRESS_VALUE_PAIR` | Existing `_GVCP_REGISTER_ADDRESS` and new `_GVCP_REGISTER_VALUE` | `nAddress`, `nValue`; multi-register camera writes. |
| `_TcVnSize2_DINT` | `_DINT` | `nWidth`, `nHeight`; create before `_TcVnParamsFindRois`. |
| `_TcVnParamsFindRois` | `_TcVnSize2_DINT`, `_LREAL` | ROI size, minimum density, detection scale, maximum oversize fraction. Preserve the export's documented defaults. |
| `_TcVnParamsWalshBarcodeDetection` | Existing scalar and interpolation wrappers | Twelve members covering barcode size, contrast, filtering, channel selection, and interpolation. Preserve the export's documented defaults. |

The complete enum members, struct fields, and documented defaults are in `datatype-members.csv`. In particular, preserve signed sentinel defaults such as `nMinArea = -1` and `nChannelIndex = -1` in Walsh detection parameters.

Some API parameters use `UDINT`/`ULINT` for an options mask and describe its enum in the comment. Parameter-type matching alone misses those dependencies. Use typed options where compatible with the pack's existing conventions, with explicit bitmask conversion at the call if needed; retain a way to combine supported flags. For existing nodes, check saved-graph compatibility before changing the port datatype.

## Build the interface and buffer foundations

The 109 absent interface wrappers are fully named in `interfaces.csv`. They are not all required to make ordinary Vision functions available as graph nodes.

**Eleven missing interface datatypes directly appear in function signatures:**

- Models: `_ITcVnMlModel`, `_ITcVnColorModel`, `_ITcVnNeuralNetwork`.
- Iterators: `_ITcVnForwardIterator`, `_ITcVnRandomAccessIterator`; complete and register the existing bidirectional wrapper with these.
- Export handles: `_ITcVnBitmapExport`, `_ITcVnDataExport`.
- Callbacks: `_ITcVnCustomContainerOperation_ITcVnContainer`, `_ITcVnCustomContainerOperation_ITcVnForwardIterator`, `_ITcVnCustomElementCondition_ITcVnContainer`, `_ITcVnCustomElementCondition_ITcVnForwardIterator`.

Also plan `_ITcVnIteratorBase` and `_ITcVnIteratorCopyCreator` to expose iterator base operations and independent iterator copies where needed. For each public interface datatype, add its appropriate `I_InterfaceDatatype_<Type>` contract and resolve/copy/reference support, following the image and container datatype pattern.

**An additional generic interface adapter is needed for `ITcUnknown`.** This type is defined outside the export's interface list but appears in 34 missing function signatures, including conversions, timestamps, and feature operations. Provide a checked, reference-counted wrapper or adapt the existing graph interface abstraction to supply it. The checked-out sibling core/graph/PLC-pack sources contain `_PVOID` support but no `_ITcUnknown` wrapper by that name; confirm the packaged dependency versions before deciding where to add the adapter.

Interface wrappers need explicit ownership rules for stored values, borrowed references, replacements, cloning, and destruction. Copying an interface pointer requires maintaining its reference count; release retained pointers when their owner is destroyed. These requirements follow Beckhoff's [interface pointer guidance](https://infosys.beckhoff.com/content/1033/tf7xxx_tc3_vision/5502731787.html) and [FW_SafeRelease documentation](https://infosys.beckhoff.com/content/1033/tcplclib_tc3_module/1900190219.html). Callback wrappers additionally need a concrete implementation supplied by PLC application code or a defined graph callback adapter; a bare stored interface will not perform a callback.

Nineteen missing functions declare `PVOID` parameters. A `_PVOID` scalar alone does not define the pointed-to memory's lifetime, capacity, or element count. Reuse a suitable existing buffer facility if available in the selected dependency versions; otherwise create an owned buffer/array adapter with bounded access. It must cover creation from arrays, binary exports, matrix data, and memory/register operations. Keep raw memory addresses out of persistent graph values. Some pointer parameters refer to interfaces or typed arrays rather than raw byte buffers; inspect each signature instead of treating every pointer identically.

The remaining absent interface wrappers are **74 typed access adapters** (`ITcVnAccess_*`, `ITcVnRandomAccess_*`) and **22 device, image-provider, notification, export, timestamp, or other infrastructure interfaces**. Plan them as an advanced parity phase. Existing `GetAt`, `SetAt`, and other function nodes already cover many typed access operations. Do not create duplicate public method nodes merely because the corresponding low-level interface exists. If full low-level interface access is required, build and register all listed adapters and expose the useful methods through explicit facades; record any intentionally internal interfaces as such.

## Implement the missing function families

The missing-source total breaks down as follows. These licence labels are taken directly from the supplied API export; they do not indicate which licences are installed locally.

| Export licence family | New function wrappers | Main work |
| --- | ---: | --- |
| TC3 Vision Base | 110 | Image/container operations, filters, remapping, polarization, regions, buffers/exports, iterators, callbacks, timestamps, watchdog control. |
| TC3 Vision Metrology 2D | 27 | Calibration variants, linescan calibration, coordinate transforms, edge/arc/ellipse location, distance and angle measurement. |
| TC3 Vision Matching | 14 | Reference-keypoint matching variants, contour matching, template matching expert variants. |
| TC3 Vision Code Reading | 5 | Walsh barcode analysis/detection and barcode/Data Matrix ROI expert reading. |
| TC3 Machine Learning Realtime Inference | 58 | Model construction, training, inference, clustering, scaling, transforms, colour models. |
| TC3 Neural Network Realtime Inference | 11 | Single/multiple input/output execution, layer outputs, layer-name queries. |

Use the complete missing-function list rather than these examples to determine batch membership. Add `Node_<exact API function name>` for each ordinary function, retaining suffixes such as `Exp`, `Exp2`, `_Point`, `_Container`, and typed overload suffixes. Those identify distinct API entries.

Recommended order within the function work:

1. **Functions using existing graph datatypes:** fill expert-variant gaps around existing nodes, ordinary filters and colour/image operations, contour and template matching. The eight image/matching functions in the second-batch progress section now have registered source wrappers. Start subsequent batches with signatures requiring no new ownership mechanism. Custom and separable custom filters depend on the disabled matrix wrapper and belong after the phase-2 buffer work.
2. **New options and struct consumers:** sorting, salient features, `FindRois`, `MergeRegions`, Walsh barcode detection, polarized-image processing, and axis-aligned edge selection. Build the datatype prerequisites first.
3. **Calibration and measurement:** implement the missing calibration, linescan, coordinate transformation, and expert metrology functions together with known-coordinate fixtures. Preserve units, coordinate conventions, and all returned arrays/containers.
4. **Iterators, callbacks, buffers, and generic interfaces:** add the missing iterator/container functions, conditional copying, custom element operations, array creation/export, matrix initialization/multiplication, JPEG/BMP export, and timestamp/conversion nodes once their ownership adapters are ready.
5. **Machine learning and neural networks:** land usable pipelines. Pair model/network loading with execution so graph users can obtain the required handles. Implement constructors and training before prediction examples; add feature scaling/transforms, cluster/novelty results, and layer-name/multiple-output handling in coherent batches.

Each new node requires the project compile entry, prototype declaration and graph-category registration in `VisionNodePack`, cloning, graph ports/parameters, execution, and meaningful pre-execution checks. Prefer the existing category of the nearest related function. Create explicit categories for new model, neural-network, and polarization families where necessary.

Review parameter directions together with comments. The API often describes a result as `Reference To ITcVnImage` with direction `In`; it still needs to be exposed as the graph's result. Similarly, read `InOut` scalars/structs and `Out` parameters carefully. Preserve `hrPrev` failure chaining and surface the function result. Use the documented defaults for expert parameters and verify image/container element types, dimensions, and counts appropriate to the operation.

### Existing helper coverage and watchdog scope

Four functions in the missing-node list already have internal call sites:

- `F_VN_CreateImageFromArray` and `F_VN_ExportImage` are used inside `_ITcVnImage`. These uses do not provide standalone graph nodes; reuse their ownership lessons when adding the nodes.
- `F_VN_StartRelWatchdog` and `F_VN_StopWatchdog` are used by `WatchdogCheckExtension` around `VisionNode` execution.

The five missing standalone watchdog functions are `F_VN_StartAbsWatchdog`, `F_VN_StartAbsWatchdogExp`, `F_VN_StartRelWatchdog`, `F_VN_StartRelWatchdogExp`, and `F_VN_StopWatchdog`. Recommend extending the existing watchdog extension for these modes and diagnostics first. If standalone watchdog nodes are required for strict function-node parity, use an execution design that does not automatically start/stop another watchdog around those nodes. Record this choice explicitly in the coverage checklist; the five entries must not silently disappear from the backlog.

## Implement stateful function-block facades

No `FB_VN_*` wrapper is currently available through the node factory. Twenty-four are absent and the initialization wrapper is disabled. One block may need a facade with several commands or cooperating nodes; the 25 blocks are not an estimate of exactly 25 final graph nodes.

| Facade family | Complete API block list | Prerequisites |
| --- | --- | --- |
| Initialization | `FB_VN_InitializeFunction` | Repair the existing implementation and define busy/error/timeout handling. |
| Image/container files | `FB_VN_ReadImage`, `FB_VN_WriteImage`, `FB_VN_ReadContainer`, `FB_VN_WriteContainer` | Image/container wrappers, path and trigger parameters, operation state. |
| Calibration files | `FB_VN_ReadCalibrationPattern`, `FB_VN_ReadCalibrationResult`, `FB_VN_WriteCalibrationResult` | Calibration arrays/containers and a consistent representation of a loaded result. |
| Model/network files | `FB_VN_ReadMlModel`, `FB_VN_WriteMlModel`, `FB_VN_ReadNeuralNetwork` | Model/network interface wrappers; schedule these alongside inference nodes. |
| Camera acquisition | `FB_VN_FileSourceControl`, `FB_VN_GevCameraControl`, `FB_VN_SimpleCameraControl` | Device association, acquisition state, trigger/recovery policy, image ownership. |
| Camera memory | `FB_VN_ReadMemory`, `FB_VN_WriteMemory` | Device association and owned buffers with bounded sizes. |
| Register reads | `FB_VN_ReadRegister_REAL`, `FB_VN_ReadRegister_UDINT`, `FB_VN_ReadRegister_ULINT` | Device association and register address wrappers. |
| Register writes | `FB_VN_WriteRegister_REAL`, `FB_VN_WriteRegister_UDINT`, `FB_VN_WriteRegister_ULINT`, `FB_VN_WriteRegisters_UDINT` | Address/value pairs and owned storage for multi-register writes. |
| Stateful matching | `FB_VN_GeneralizedHoughBallard`, `FB_VN_SSIM` | Retained template/reference, parameter setup, and explicit reset/reconfiguration behavior. |

For asynchronous blocks, retain the FB instance across calls, trigger an operation once, continue servicing it while busy, and expose completion/error information without retriggering accidentally. The repository has a `VisionHardwareNode` base, but its suitability for servicing operations across cycles must be checked against the graph scheduler before choosing the final base class. Method-based camera and matching blocks need explicit commands and state rather than the cyclic `bBusy` contract being applied indiscriminately.

Plan file/model facades early enough to support the function pipelines. Camera and register integration can follow as a separate hardware-tested batch. Real camera register writes belong in those controlled integration tests, not the general unit-test startup path.

## Delivery sequence and acceptance criteria

| Phase | Deliverable | Dependencies and completion check |
| --- | --- | --- |
| 0 | Reproducible TwinCAT 5.10.2 development/test baseline | Correct dependency resolution; existing library and test PLC build; baseline TcUnit results. |
| 1 | Existing wrapper repairs and 15 value datatypes | Enum/member construction and round trips; triangle area output; all new datatypes discoverable. Matrix and initialization activation wait for the relevant phase-2 foundations. |
| 2 | Interface ownership, iterator contracts, buffer/matrix design, asynchronous operation pattern | Copy/reference/release and buffer lifetime tests; activate matrix multiplication and initialization once these checks pass. |
| 3 | Ordinary image/container, matching, code-reading, calibration, metrology and polarization function batches | Datatype prerequisites from phases 1–2; representative numerical/image fixtures and node discovery for each batch. |
| 4 | ML/NN datatypes, loading facades, constructors/training/execution pipelines | Phase 2 handles; end-to-end model/network loading and results; licence-dependent test results recorded. |
| 5 | Remaining file/camera/memory/register/stateful-matching facades | Asynchronous scheduling proven; simulated file/error tests and separate camera integration tests. |
| 6 | Remaining low-level interface adapters and explicit watchdog coverage decision | Every interface/function entry either implemented and registered or documented as intentionally internal/extension-managed. Strict standalone parity requires implementing any remaining entries. |
| 7 | Release | Full solution build and runtime validation; updated docs/examples/changelog; rebuild and replace the root `.library` from validated source. |

For each implementation batch:

- Run the inventory and check for absent compile entries, excluded wrappers, unregistered prototypes/datatypes, and missing enum/member labels. The script checks unique declarations and prototype registration paths as well as referenced source-file existence.
- Test behavior rather than only mirroring constructor code: enum parsing/serialization, struct copy/reference behavior, graph save/load compatibility, image/container ownership, failure chaining, and output values against known fixtures or a direct API call on the same input.
- For iterator/model/buffer wrappers, test replacement, cloning, cleanup, null values, and repeated graph execution to catch leaks or stale references. Use independent iterator positions where a clone promises independent traversal.
- For asynchronous facades, test completion over multiple cycles, timeout, failure, re-trigger after completion, and reset while an operation is in progress.
- Run the required TwinCAT build and applicable TcUnit/integration tests. Record unavailable hardware, model assets, or licences as untested coverage rather than passing results.

Completion means the checklist has a deliberate disposition for every API entry, all intended public nodes and datatypes are discoverable and usable, and the published library is built from that validated source. A CSV row becoming “registered” is necessary but insufficient for completion.

## Review boundaries

This audit parsed the entire supplied API and all 1,078 library `.TcPOU` files, checked project compilation settings and pack registrations, compared enum/member labels, and checked the named arguments of existing function calls. It also inspected representative node/datatype implementations, the extension/base classes, dependency settings, and the test structure. The generated results account for all exported functions, named types, interfaces, constants, and function blocks.

The audit is a structural comparison, not a complete semantic review of every precondition, default, parameter expression, or algorithm. The HTML does not provide every enum's numeric value or all runtime constraints; use native constants and validate against the installed target library during implementation. TwinCAT compilation, TcUnit execution, real-time behavior, and hardware tests were not run in this Linux workspace. The existing compiled `.library` was not rebuilt or used as proof of source compatibility.
