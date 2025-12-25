# CrowdStrike Vulnerability Enrichment - Testing Guide

## Overview
This guide covers testing the vulnerability enrichment feature integrated into the CrowdStrike connector.

## Prerequisites
1. OpenCTI instance running and accessible
2. MITRE CVE connector running (to populate base CVEs)
3. CrowdStrike Spotlight API credentials
4. Docker installed

## Test Scenarios

### Test 1: Verify No Breaking Changes (Existing Scopes)
**Objective:** Ensure existing connector functionality (actor, report, indicator, yara_master, snort_suricata_master) still works

**Steps:**
1. Run connector with existing scopes only (NO vulnerability scope)
2. Verify actors, reports, indicators import successfully
3. Check logs for errors

**Expected Result:** All existing importers work without errors

### Test 2: Vulnerability Enrichment Only
**Objective:** Test vulnerability enrichment in isolation

**Steps:**
1. Build Docker image:
   ```bash
   docker build -t crowdstrike-connector:vulnerability-test .
   ```

2. Run with vulnerability scope only:
   ```bash
   docker-compose -f docker-compose.test.yml up
   ```

3. Monitor logs for:
   - Successful authentication with CrowdStrike API
   - Vulnerability fetching from Spotlight API
   - CVE lookups in OpenCTI
   - Label additions
   - External reference additions

4. Verify in OpenCTI UI:
   - Navigate to Analyses > Vulnerabilities
   - Filter by labels containing "crowdstrike"
   - Check if CVEs have new labels:
     - `crowdstrike-spotlight`
     - `crowdstrike-exploit-verified` or `crowdstrike-exploit-poc`
     - `crowdstrike-status-open`
     - `crowdstrike-high-priority` (for high CVSS + exploit)
   - Check external references link to CrowdStrike Falcon console

**Expected Results:**
- Enriched count > 0
- Skipped count shows CVEs not in OpenCTI
- Error count = 0
- Labels visible in UI
- External references clickable

### Test 3: Combined Scopes
**Objective:** Test vulnerability enrichment alongside other scopes

**Steps:**
1. Update docker-compose.test.yml:
   ```yaml
   CROWDSTRIKE_SCOPES=actor,report,vulnerability
   ```

2. Run connector
3. Verify all scopes work correctly

**Expected Result:** No conflicts, all importers complete successfully

### Test 4: Configuration Options
**Objective:** Test different configuration parameters

**Test 4a: Min CVSS Score**
```yaml
CROWDSTRIKE_VULNERABILITY_MIN_CVSS_SCORE=9.0
```
Expected: Only CVE with CVSS >= 9.0 enriched

**Test 4b: Include Closed**
```yaml
CROWDSTRIKE_VULNERABILITY_INCLUDE_CLOSED=true
```
Expected: Both open and closed vulnerabilities enriched

**Test 4c: Start Timestamp**
```yaml
CROWDSTRIKE_VULNERABILITY_START_TIMESTAMP=1704067200  # 2024-01-01
```
Expected: Only vulnerabilities created/updated after 2024-01-01 enriched

## Verification Checklist

### Code Quality
- [x] All Python files compile without syntax errors
- [x] Follows existing connector patterns (BaseImporter, builder pattern)
- [x] Proper error handling
- [x] Logging at appropriate levels

### Functionality
- [ ] Vulnerability enricher initializes correctly
- [ ] Spotlight API client authenticates successfully
- [ ] Vulnerabilities fetched with correct FQL filter
- [ ] Existing CVEs found in OpenCTI
- [ ] Labels added successfully
- [ ] External references created
- [ ] State management works (timestamp tracking)
- [ ] No duplicate CVEs created

### Non-Breaking Changes
- [ ] Existing scopes (actor, report, indicator, yara_master, snort_suricata_master) unaffected
- [ ] Docker image builds successfully
- [ ] Connector starts without errors when vulnerability scope not enabled
- [ ] Configuration backward compatible

### Documentation
- [x] README updated with vulnerability configuration
- [x] Configuration table includes vulnerability options
- [x] Vulnerability Enrichment section added
- [ ] Code comments clear and helpful

## Test Configuration

**Test Environment:**
- OpenCTI URL: http://localhost:8080
- OpenCTI Token: (from environment)
- CrowdStrike API: https://api.crowdstrike.com
- CrowdStrike Client ID: (from environment)
- Network: opencti_default

**Test Docker Compose:**
See `docker-compose.test.yml` for test configuration

## Known Limitations
1. Requires MITRE CVE connector to populate base CVEs first
2. Only enriches high-value CVEs (CVSS >= 7.0 OR exploit status OR open status)
3. External reference creation may need adjustment based on OpenCTI API version

## Troubleshooting

### Issue: "CVE not found in OpenCTI"
**Cause:** MITRE connector hasn't imported that CVE yet
**Solution:** Ensure MITRE CVE connector is running and has completed at least one import cycle

### Issue: "Error fetching vulnerabilities"
**Cause:** CrowdStrike API authentication failed or invalid filter
**Solution:** Verify CrowdStrike credentials and check API permissions include Spotlight

### Issue: "Error adding label"
**Cause:** OpenCTI API version mismatch or permission issue
**Solution:** Check OpenCTI connector helper version and API compatibility

## Success Criteria
- ✅ Docker image builds without errors
- ✅ Connector starts successfully
- ✅ Vulnerabilities fetched from CrowdStrike API
- ✅ At least 10 CVEs enriched with labels
- ✅ External references visible in OpenCTI UI
- ✅ No errors in connector logs
- ✅ Existing scopes continue to work
- ✅ State persisted correctly for next run

