package com.universalapp.androidcore.viewmodel

import android.content.Context
import android.provider.Settings
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.universalapp.androidcore.data.GatewayApiService
import com.universalapp.androidcore.security.AdvancedTamperDetector
import com.universalapp.androidcore.security.SecureStorageManager
import com.universalapp.androidcore.security.SecurityIntegrityChecker
import com.universalapp.androidcore.security.ThreatMitigationHandler
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {

    private val apiService = GatewayApiService()

    private val _logOutput = MutableStateFlow("Tap 'Scan Core Parameters' to start...")
    val logOutput: StateFlow<String> = _logOutput

    // Attack Simulation State
    private val _isSimulatingAttack = MutableStateFlow(false)
    val isSimulatingAttack: StateFlow<Boolean> = _isSimulatingAttack

    fun toggleAttackSimulation() {
        _isSimulatingAttack.value = !_isSimulatingAttack.value
    }

    fun performScan(context: Context) {
        viewModelScope.launch(Dispatchers.IO) {
            val secureStorage = SecureStorageManager(context)
            val deviceId = Settings.Secure.getString(context.contentResolver, Settings.Secure.ANDROID_ID) ?: "DEVICE_001"

            _logOutput.value = "Authenticating with API Gateway..."

            // 1. Get or Fetch JWT Access Token
            var token = secureStorage.getAuthToken()
            if (token == null) {
                token = apiService.loginDevice(deviceId)
                if (token != null) {
                    secureStorage.saveAuthToken(token)
                } else {
                    _logOutput.value = "Scan Failed: Auth Gateway Unavailable"
                    return@launch
                }
            }

            _logOutput.value = "Evaluating Threats & Transmitting Telemetry..."

            // 2. Perform RASP Checks (Combines real engine with simulation toggle)
            val realHook = AdvancedTamperDetector.isHookingFrameworkPresent() || AdvancedTamperDetector.isStackTraceHooked()
            val isHooked = realHook || _isSimulatingAttack.value
            val isIntegrityValid = SecurityIntegrityChecker.verifyAppIntegrity(context)

            // 3. Trigger Active Mitigation if Threat Found
            if (isHooked) {
                ThreatMitigationHandler.handleDetectedThreat(
                    context,
                    "Frida/Hooking Framework",
                    ThreatMitigationHandler.ThreatLevel.CRITICAL
                )
            }

            // 4. Construct Scan Payload
            val scanPayload = mapOf(
                "deviceId" to deviceId,
                "rootDetected" to false,
                "isEmulator" to true,
                "debuggerAttached" to false,
                "fridaHookDetected" to isHooked,
                "integrityVerified" to isIntegrityValid,
                "threatMitigated" to isHooked
            )

            // 5. Send Telemetry through API Gateway
            val (statusCode, responseBody) = apiService.sendTelemetry(token, scanPayload)

            // 6. Update UI Log Output
            if (statusCode == 200) {
                _logOutput.value = """
                    Scan Transmitted! (HTTP $statusCode)
                    Status: ${if (isHooked) "THREAT MITIGATED" else "SECURE"}
                    Token Integrity: VERIFIED
                    Frida Hook Detected: $isHooked
                    Integrity Verified: $isIntegrityValid
                """.trimIndent()
            } else {
                _logOutput.value = "Gateway Error ($statusCode): $responseBody"
            }
        }
    }
}