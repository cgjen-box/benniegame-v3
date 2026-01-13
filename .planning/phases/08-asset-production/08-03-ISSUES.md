# UAT Issues: Phase 8 Plan 3

**Tested:** 2026-01-13
**Source:** .planning/phases/08-asset-production/08-03-SUMMARY.md
**Tester:** User via /gsd:verify-work

## Open Issues

### UAT-001: Lottie character animations not fully visible to user

**Discovered:** 2026-01-13
**Phase/Plan:** 08-03
**Severity:** Major
**Feature:** Lottie animation integration in LoadingView
**Description:** User reports characters are blank/missing on LoadingView despite Claude's screenshots showing animations rendering. Possible display, timing, or device-specific issue.
**Expected:** Bennie Bear and Lemminge characters should be clearly visible and animating on the loading screen
**Actual:** User sees blank/missing characters
**Notes:**
- Claude's simulator screenshots show animations working
- Build succeeds with no errors
- 13 Lottie JSON files are in app bundle
- May be timing issue (loading screen only shows ~2 seconds)
- May need further investigation of LottieView sizing/rendering

## Resolved Issues

[None yet]

---

*Phase: 08-asset-production*
*Plan: 03*
*Tested: 2026-01-13*
