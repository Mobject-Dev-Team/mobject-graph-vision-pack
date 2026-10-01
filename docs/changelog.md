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
- Added twelve measurement nodes completing the expert edge metrology family: LocateAxisAlignedEdges/Exp, LocateCircularArcExp/Exp2, LocateEdgeExp2, LocateEdgesExp2, LocateEllipseExp2, MeasureAngleBetweenEdgesExp/Exp2, MeasureEdgeDistanceExp2, and MeasureMinEdgeDistanceExp/Exp2. Optional edge-point, edge-strength, contour, distance, and derivative outputs may be left unconnected.
- Added the eight reference-keypoint matching nodes, closing the TC3 Vision Matching backlog: FindReferenceKeyPointsInImage/Exp plus the AKAZE, BRISK, and ORB variants and their expert forms. Together with the MatchDescriptors nodes these locate a known reference image in a source image and return its perspective transformation.
- **breaking** the elementwise container statistics nodes (Max/Min/Median, 96 typed variants) and LocateEllipseExp no longer register their result as an input port. The result was offered as both an input and an output, and because an input port aliases the upstream node's storage, connecting it made the call write its result into whichever node fed the edge. The result remains available as an output. A saved graph breaks only if it actually connected one of these input ports; none of the shipped examples do, but such a graph fails to deserialize as a whole rather than dropping the one link.
- ClipLineToBoundary (all three variants) now exposes aStartPoint and aEndPoint as outputs. They are documented as returning the clipped points but were registered as inputs only, so the node's results were unreachable from its outputs. The inputs are kept so existing saved links still resolve.
- SetImageChannel and WhiteBalance keep their ipDestImage input. Writing into a supplied destination is how the Golden Template and Colour Balance examples compose an image one channel at a time, sequenced with hrPrev, so it is a supported idiom rather than an oversight.
- Added the five code reading nodes, closing the TC3 Vision Code Reading backlog: AnalyzeBarcodeWalsh and DetectBarcodesWalsh, which pair to tune and then run Walsh barcode detection, plus ReadBarcodeRoi/Exp and ReadDataMatrixCodeRoiExp. The ROI readers accept only the barcode types their documentation lists as supported.
- The audit tool now reports write-through input ports (`port-write-through.csv`, counted in `summary.json`), so ports whose result the native call writes back through an input edge are a tracked category rather than something to rediscover.
- Added fifteen calibration and coordinate transformation nodes, so a calibration result can now be used: TransformCoordinatesImageToWorld, TransformCoordinatesWorldToImage and TransformCoordinatesPlanar (point and container forms each), ImagePointsWorldDistance, CalibrateCameraManually/Exp, CalibrateCameraPlanarExp, DetectPatternPoints2, DetectPatternPointsExp, SortAxisAlignedPatternPoints, and DecomposeHomography/Exp. SortAxisAlignedPatternPoints sorts its input container in place, like ReverseContainer; sequence its consumers with hrPrev.
- The distributed `.library` was last rebuilt in `7d67de2`; the calibration nodes added since still need a TwinCAT build. Runtime validation and comprehensive tests remain pending.

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
