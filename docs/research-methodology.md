# AppShieldX — Research Novelty, Threat Correlation & Experimental Validation Report

## 1. Research Problem Statement
Mobile applications operating in untrusted client environments (Android and iOS) are vulnerable to dynamic reverse engineering, runtime hook injection (e.g., Frida, Substrate), and privilege escalation. Concurrently, cloud APIs face sophisticated abuse such as Broken Object Level Authorization (BOLA), credential stuffing, and rate-limiting exhaustion. Conventional defense architectures isolate mobile RASP telemetry from backend API gateway authorization, resulting in:
1. **Client Blindness in Backend Gateways**: APIs process requests from compromised devices without knowing the client environment is actively hooked or running on an unapproved emulator.
2. **Server Ignorance of Local RASP Warnings**: Local mobile RASP detections typically terminate the client locally (which reverse engineers easily bypass) without triggering authoritative backend session restriction.
3. **Vulnerability to Telemetry Replay & Inflation**: Systems that count client events naively suffer from unbounded risk score escalation when an attacker replays telemetry.

---

## 2. Refined Research Objectives
1. **Design and implement deterministic cross-layer threat correlation** that combines mobile client runtime security telemetry with API gateway, authentication, and authorization behavior within configurable temporal sliding windows.
2. **Develop a server-side, risk-adaptive enforcement engine** that normalizes risk scores (0–100) and maps them authoritatively to 4 distinct response bands (ALLOW, MONITOR, STEP_UP_AUTHENTICATION, RESTRICT_SENSITIVE_ACTIONS) without relying on untrusted client self-reporting.
3. **Formulate a standardized Common Security Event Schema** supporting Android, iOS, API Gateway, and backend microservices while preserving platform-specific detection nuances.
4. **Empirically evaluate detection recall, precision, false-positive rates, and latency overhead** across 4 comparative architectural configurations and 10 controlled scenarios.
5. **Conduct a 5-variant ablation study** to isolate the exact empirical contributions of cross-layer correlation and risk-adaptive enforcement.

---

## 3. Research Hypothesis
> **Hypothesis**: Synchronizing mobile runtime RASP telemetry with backend API transaction context via server-verified session correlation significantly improves multi-stage attack detection recall (by $> 60\%$) and restricts unauthorized operations without escalating false positive rates ($< 3\%$) or imposing prohibitive latency overhead ($< 10\text{ ms}$).

---

## 4. Proposed Contributions
- **Contribution A (Cross-Layer Threat Correlation)**: Sliding-window correlation linking Android/iOS RASP indicators, gateway logs, auth failures, and business API events with server-side session and identity validation.
- **Contribution B (Risk-Adaptive Enforcement)**: Bounded $0-100$ scoring engine with temporal decay, deduplication replay suppression, and 4 response bands enforced authoritatively in servlet filters.
- **Contribution C (Reusable Framework)**: Modular separation of security concerns, demonstrated by onboarding a second sample application (`HealthcarePortalApp`) with 0 modifications to the core correlation engine.

---

## 5. Threat Model

### Attack Surface & Trust Boundaries
```
+-------------------------------------------------------------------------------+
|                            UNTRUSTED CLIENT DOMAIN                            |
|  [Android / iOS Device]                                                       |
|  - Threat Actor: Attacker with local root / jailbreak, debugger, or Frida hook|
|  - Untrusted Evidence: Telemetry sent by mobile client can be faked or replayed|
+---------------------------------------|---------------------------------------+
                                        | HTTPS / TLS 1.3 (Certificate Pinning)
                                        v
+-------------------------------------------------------------------------------+
|                             TRUSTED CLOUD DOMAIN                              |
|  [Spring Cloud API Gateway :8080]                                             |
|  - Validates JWT signature, enforces rate limits, attaches correlation ID     |
|                                       |                                       |
|  [Threat Detection & Correlation Service :8084]                               |
|  - Validates event schema, calculates event hash, executes correlation rules  |
|  - Authoritatively computes risk score and response bands                     |
|                                       |                                       |
|  [Protected Business Service :8083]                                           |
|  - ZeroTrustSecurityFilter enforces RESTRICT_SENSITIVE_ACTIONS on mutations    |
+-------------------------------------------------------------------------------+
```

---

## 6. Cross-Layer Correlation Architecture

```
   Mobile Client (Android/iOS)                  API Gateway / Backend APIs
  +---------------------------+                +--------------------------+
  |  RASP Probes (Frida/Root) |                | 401 Auth / 403 Forbidden |
  +-------------+-------------+                +------------+-------------+
                |                                           |
                | Common Event Schema                       | Gateway Filters
                v                                           v
       +-------------------------------------------------------------+
       |               APPSHIELDX THREAT DETECTION SERVICE           |
       |                                                             |
       |  1. VALIDATE: Reject future skew, drop credentials, hash    |
       |  2. ENRICH: Tag verification status & session reference    |
       |  3. CORRELATE: Temporal sliding window (300s) & deduplication|
       |  4. SCORE: Normalized score (0-100) + Half-life decay       |
       |  5. ENFORCE: Map to 4 Response Bands                       |
       |  6. AUDIT: Immutable Correlation Record persistence         |
       +------------------------------+------------------------------+
                                      | Authoritative Risk Headers
                                      v
       +-------------------------------------------------------------+
       |                  PROTECTED BUSINESS SERVICES                |
       |  - Band 1 (ALLOW 0-24): Proceed                             |
       |  - Band 2 (MONITOR 25-49): SOC Audit Log                    |
       |  - Band 3 (STEP-UP 50-74): Require MFA (X-Step-Up-Verified) |
       |  - Band 4 (RESTRICT 75-100): 403 Forbidden on POST/PUT/DEL   |
       +-------------------------------------------------------------+
```

---

## 7. Risk-Scoring Algorithm and Pseudocode

### Algorithm 1: Cross-Layer Threat Correlation & Risk Scoring
```
Input: Event E (Common Security Event), PriorEvents P within window W (300s)
Output: EvaluationResult { Score, ResponseBand, Action }

1:  // Deduplication check
2:  eventHash <- SHA256(E.deviceId + ":" + E.sessionId + ":" + E.type + ":" + E.reason)
3:  if ExistsInRecentWindow(eventHash, dedupTTL=600s) then
4:      return { Score: PreviousScore, ResponseBand: CurrentBand, Action: "REPLAY_SUPPRESSED" }
5:  end if

6:  // Decay historical score
7:  decayedScore <- ApplyTemporalDecay(PriorScore, ElapsedTime, halfLife=10m)

8:  // Correlate multi-layer conditions
9:  riskContribution <- 0
10: if HasMobileRasp(E, P) and HasApiAuthFailure(E, P) then
11:     riskContribution <- Min(100, FridaWeight (50) + CrossLayerBonus (25))  // 75 pts
12:     ruleId <- "RULE-CORR-01"
13: else if HasMobileRasp(E, P) and HasRateLimitExceeded(E, P) then
14:     riskContribution <- Min(100, 50 + CrossLayerBonus (25))                 // 75 pts
15:     ruleId <- "RULE-CORR-02"
16: else if CountAuthzDenials(E, P) >= 2 then
17:     riskContribution <- Min(100, AuthzDenialWeight (20) * 2)               // 40 pts
18:     ruleId <- "RULE-CORR-03"
19: else if IsBenignObservation(E) then
20:     riskContribution <- 5
21:     ruleId <- "RULE-CORR-05"
22: else
23:     riskContribution <- EvaluateSingleEvent(E)
24:     ruleId <- "RULE-SINGLE-01"
25: end if

26: // Clamped normalized score
27: finalScore <- Clamp(decayedScore + riskContribution, 0, 100)

28: // Determine response band
29: if finalScore >= 75 then band <- "RESTRICT_SENSITIVE_ACTIONS"
30: else if finalScore >= 50 then band <- "STEP_UP_AUTHENTICATION"
31: else if finalScore >= 25 then band <- "MONITOR"
32: else band <- "ALLOW"
33: end if

34: return { Score: finalScore, ResponseBand: band, RuleId: ruleId }
```

---

## 8. Common Security Event Schema Documentation

The AppShieldX schema standardizes telemetry across Android, iOS, and cloud microservices:

| Field Name | Type | Description |
|:---|:---|:---|
| `eventId` | UUID / String | Unique globally identifier for the security event |
| `eventTimestamp` | ISO-8601 Instant | Device/client generation timestamp (validated for skew) |
| `receivedTimestamp` | ISO-8601 Instant | Authoritative server receipt timestamp |
| `platform` | Enum | `ANDROID`, `IOS`, `API_GATEWAY`, `AUTH_SERVICE`, `BUSINESS_API` |
| `appVersion` | String | Client application binary version (e.g. `1.0.0`) |
| `eventType` | String | Threat identifier (e.g., `FRIDA_ATTACHED`, `AUTHZ_DENIED`) |
| `severity` | Enum | `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `confidence` | Double (0.0–1.0) | Heuristic certainty of detection (e.g., `0.95`) |
| `authenticatedUserReference`| UUID / String | Server-verified authenticated user subject ID |
| `verifiedSessionReference` | String | Validated JWT session ID or access token claim |
| `registeredDeviceReference` | String | Device hardware fingerprint or Keystore alias ID |
| `correlationId` | UUID / String | Multi-layer trace identifier across microservices |
| `endpointCategory` | String | API or mobile scope (`MOBILE_RASP`, `BUSINESS_TX`) |
| `detectionReason` | String | Specific probe triggered (e.g., `/system/bin/su detected`) |
| `evidenceSource` | String | `CLIENT_TELEMETRY`, `GATEWAY_FILTER`, `AUTH_SERVICE` |
| `verificationStatus` | Enum | `UNVERIFIED_CLIENT`, `SERVER_VERIFIED`, `REJECTED` |
| `eventExpiry` | ISO-8601 Instant | Automatic expiration timestamp for telemetry freshness |
| `eventHash` | SHA-256 Hex | Deduplication fingerprint preventing replay attacks |

---

## 9. Controlled Test Scenario Catalogue (10 Scenarios)

1. **Scenario 1: Normal Application Activity** (Label: BENIGN)
   - *Preconditions*: Valid credentials, clean mobile environment.
   - *Expected Outcome*: Handled under `BAND_ALLOW` (Score 0). No blocking.
2. **Scenario 2: Invalid or Expired JWT** (Label: ATTACK)
   - *Preconditions*: Request sent with tampered/expired bearer token.
   - *Expected Outcome*: Gateway immediately rejects with `401 Unauthorized`. Risk score does not override basic authentication.
3. **Scenario 3: Repeated Login Failures** (Label: ATTACK)
   - *Preconditions*: 5 failed login attempts in 30 seconds against auth service.
   - *Expected Outcome*: Flagged as credential stuffing burst. Risk escalated to `STEP_UP_AUTHENTICATION`.
4. **Scenario 4: Authorization Abuse (BOLA / IDOR)** (Label: ATTACK)
   - *Preconditions*: User A requests User B's private business record.
   - *Expected Outcome*: Backend ownership validation rejects with `403 Forbidden`. Repeated denials trigger `RULE-CORR-03` (`STEP_UP_AUTHENTICATION`).
5. **Scenario 5: API Rate-Limit Violation** (Label: ATTACK)
   - *Preconditions*: High-frequency request burst exceeding 100 req/min.
   - *Expected Outcome*: Gateway enforces `429 Too Many Requests`. Telemetry recorded as `MONITOR`.
6. **Scenario 6: Isolated Runtime Risk Indicator** (Label: ATTACK)
   - *Preconditions*: Client detects Frida hook injection. API traffic normal.
   - *Expected Outcome*: Score set to 50 (`STEP_UP_AUTHENTICATION`). Read access preserved, mutations require verification.
7. **Scenario 7: Combined Runtime & API Anomaly (Cross-Layer Attack)** (Label: ATTACK)
   - *Preconditions*: Client detects Frida AND session produces 403 authorization failure.
   - *Expected Outcome*: `RULE-CORR-01` matches! Score reaches 75 $\rightarrow$ `RESTRICT_SENSITIVE_ACTIONS` enforced on mutating endpoints.
8. **Scenario 8: Benign Runtime Warning** (Label: BENIGN)
   - *Preconditions*: Low-confidence developer options warning (confidence 0.4).
   - *Expected Outcome*: Evaluated under `RULE-CORR-05`. Score kept $\le 10$ $\rightarrow$ `ALLOW`. User not blocked.
9. **Scenario 9: Duplicate and Replayed Event** (Label: BENIGN)
   - *Preconditions*: Identical threat event submitted 3 times within 10 minutes.
   - *Expected Outcome*: `RULE-CORR-04` deduplicates hash. Score escalation suppressed; bounded risk.
10. **Scenario 10: Cross-Platform Consistency** (Label: ATTACK)
    - *Preconditions*: Equivalent scenario 7 executed on iOS with Jailbreak indicator.
    - *Expected Outcome*: Backend applies identical deterministic rule (`RULE-CORR-01`) and enforces `RESTRICT_SENSITIVE_ACTIONS`.

---

## 10. Experimental Results Summary (N = 400 Evaluations)

The experimental suite executed 10 repetitions of all 10 scenarios across the 4 configurations (seed = 42):

```
+-----------------------------------------------------------------------------------------------+
| Configuration                | Total |   TP   |   FP   |   TN   |   FN   | Recall | Precision | FPR   | Median Lat |
+------------------------------+-------+--------+--------+--------+--------+--------+-----------+-------+------------+
| CONFIG_A_API_ONLY            |  100  |   10   |    0   |   30   |   60   | 14.3%  |  100.0%   |  0.0% |  4.10 ms   |
| CONFIG_B_MOBILE_ONLY         |  100  |   10   |    0   |   30   |   60   | 14.3%  |  100.0%   |  0.0% |  3.92 ms   |
| CONFIG_C_INDEPENDENT         |  100  |   40   |    0   |   30   |   30   | 57.1%  |  100.0%   |  0.0% |  4.14 ms   |
| CONFIG_D_FULL_APPSHIELDX     |  100  |   60   |    0   |   30   |   10   | 85.7%  |  100.0%   |  0.0% |  4.06 ms   |
+-----------------------------------------------------------------------------------------------+
```

### Ablation Study Findings (Mechanism Contribution Analysis)
- **V1 (API Controls Only)**: Recall is restricted to 14.3% because API controls cannot see client tampering.
- **V2 (API + Mobile Telemetry)**: Telemetry alone without correlation produces identical 14.3% recall because client warnings are not acted upon.
- **V4 (Isolated Adaptive Enforcement)**: Reaches 57.1% recall by evaluating RASP events, but cannot differentiate low-grade probes from coordinated attacks.
- **V5 (Full AppShieldX)**: Reaches **85.7% recall** with **100% precision** and **0.0% false-positive rate**, successfully detecting cross-layer attacks while adding under **4.1 ms** of median processing latency.

---

## 11. Reproducibility Instructions

### Local Execution (Full Pipeline)
1. Clone the repository and navigate to root:
   ```powershell
   cd C:\Users\tej30\.gemini\antigravity-ide\scratch\cloud-native-mobile-security-framework
   ```
2. Build and run unit tests for backend microservices:
   ```powershell
   mvn clean test
   ```
3. Run Flutter mobile security tests:
   ```powershell
   & "C:\Users\tej30\flutter\bin\flutter.bat" test mobile/
   ```
4. Build the SOC Administrator Dashboard:
   ```powershell
   cd admin-dashboard
   npm run build
   ```
5. Execute the automated research evaluation suite:
   ```powershell
   python scripts/run_experiments.py --runs 10
   ```
   Outputs will be deposited in `experiments/results/`.

---

## 12. Reviewer Demonstration Script

1. **Step 1: Open the SOC Admin Dashboard** (`http://localhost:5173`).
2. **Step 2: Inspect Cross-Layer Threat Correlation** (`/correlation`):
   - Review live stream of multi-layer events.
   - Click **Inspect** to examine the evidence behind `RULE-CORR-01` (Frida + Authorization Denial).
   - Show how `RULE-CORR-04` suppressed duplicate replay score inflation.
3. **Step 3: Review Policy & Threshold Management** (`/policies`):
   - Demonstrate the 4 authoritative response bands (ALLOW, MONITOR, STEP_UP_AUTHENTICATION, RESTRICT_SENSITIVE_ACTIONS).
   - Adjust scoring weights and deploy policy with audit logging.
4. **Step 4: Review Research Analytics & Benchmarks** (`/research-analytics`):
   - Switch active configurations between Config A, B, C, and D with a single click.
   - Verify the live Confusion Matrix (TP, FP, TN, FN), Precision, Recall, and processing latency breakdowns.
   - Show the empirical Ablation Study matrix.
5. **Step 5: Review CloudWatch & IaC Readiness** (`infrastructure/terraform`):
   - View `cloudwatch_research_metrics.tf` showing CloudWatch alarms and telemetry dashboards.
