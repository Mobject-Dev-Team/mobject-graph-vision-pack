# Changelog

## Unreleased — Vision 5.10.2 source work

- Added 15 value datatype wrappers and 41 enabled enum values from the Vision 5.10.2 reference. MONO14P remains disabled for the selected 5.10.3.0 build.
- Added SalientFeatures, FindRois, and MergeRegions graph nodes.
- Added eight image/matching nodes: InvertImageColorExp, NormalizeImageExp, MatchTemplateExp, MatchTemplateAndEvaluateExp, MatchDescriptorsBFExp, MatchDescriptorsKnnBFExp, MatchContours, and MatchContoursExp. Expert inputs include optional masks; template evaluation also exposes match scores.
- Added image/matching precondition checks. Regression tests are deferred to a separate branch; the initial fixtures were removed in `604c579`.
- Added ten polarization and coordinate image nodes: demosaicing, angle/degree of linear polarization, glare reduction, and Cartesian/polar angle, magnitude, and coordinate image conversions (including expert variants).
- Added eight geometric transformation nodes: ConvertMaps, RemapImage/Exp, RemapImageToLogPolarSpaceExp/Exp2, RemapImageToPolarSpaceExp/Exp2, and AlignRotatedImageRegionExp, with shared validation for supported map pairs.
- Added the enclosing-triangle area output and preserved its value when execution fails or is skipped.
- Corrected the Huber enum and BRISK member labels while keeping legacy serialized values readable.
- Preserved the Vision 5.10.3.0 resolutions, GVCP constructor fixes, and corrected merge-region option from `604c579`.
- The distributed `.library` was updated in `604c579`; the eighteen subsequent polarization/conversion/remapping nodes still need a TwinCAT build. Runtime validation and comprehensive tests remain pending.

## v0.11.0-beta

- Added nodes
- added support for mobject-graph v0.18.0
- updated to support mobject-core v0.10.0

## v0.10.0-beta

- updated to 4026.22
- added support for mobject-core v0.9.0
- added support for mobject-graph v0.17.0
- added support for mobject-graph-plc-pack v0.18.0
- 4026 unable to copy .value to .value when reference, changed to trycopyto.
- bug fix IsRoiSizeOk
- fixed container stats
- added enums

## v0.9.0-alpha

- added support for mobject-graph v0.16.0
- added support for mobject-graph-plc-pack v0.17.0
- added support for mobject-core v0.7.0

## v0.8.0-alpha

- added support for mobject-graph v0.15.0
- added support for mobject-graph-plc-pack v0.16.0
- added support for mobject-core v0.6.0
- updated support for new TryCopyContent

## v0.7.0-alpha

- added support for mobject-core v0.5.0
- added support for mobject-graph v0.14.0
- added support for mobject-graph-plc-pack v0.15.0

## v0.6.0-alpha

- added support for mobject-core v0.4.0
- added support for mobject-graph v0.12.0
- added support for mobject-graph-plc-pack v0.14.0

## v0.5.0-alpha

- added support for mobject-graph v0.11.0
- added support for mobject-graph-plc-pack v0.12.0

## v0.4.0-alpha

- added support for mobject-graph v0.10.0
- added support for mobject-graph-plc-pack v0.11.0
- added Node_F_VN_GaussianFilter

## v0.3.0-alpha

- added support for mobject-graph v0.9.0
- new style of installation using I_GraphPack
- updated to support mobject-core v0.3.0

## v0.2.0-alpha

- name change to mobject-graph-vision-pack

## v0.1.0-alpha

- Initial code
