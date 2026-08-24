package com.universalapp.androidcore.security

import android.content.Context
import com.universalapp.androidcore.data.GatewayApiService
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

object AppShieldX {

    private val apiService = GatewayApiService()

    /**
     * Public entry point to execute full RASP checks and stream telemetry to backend.
     */
    fun startProtection(context: Context, deviceId: String, onScanComplete: (Boolean) -> Unit) {
        CoroutineScope(Dispatchers.IO).launch {
            val storage = SecureStorageManager(context)

            // 1. Authenticate with backend
            var token = storage.getAuthToken()
            if (token == null) {
                token = apiService.loginDevice(deviceId)
                if (token != null) storage.saveAuthToken(token)
            }

            // 2. Perform native & runtime checks
            val isHooked = AdvancedTamperDetector.isHookingFrameworkPresent()
            val isIntegrityValid = SecurityIntegrityChecker.verifyAppIntegrity(context)

            // 3. Mitigate if threatened
            if (isHooked) {
                ThreatMitigationHandler.handleDetectedThreat(
                    context,
                    "Memory Tampering / Hooking Detected",
                    ThreatMitigationHandler.ThreatLevel.CRITICAL
                )
            }

            // 4. Send Telemetry
            if (token != null) {
                val payload = mapOf(
                    "deviceId" to deviceId,
                    "fridaHookDetected" to isHooked,
                    "integrityVerified" to isIntegrityValid,
                    "threatMitigated" to isHooked
                )
                apiService.sendTelemetry(token, payload)
            }

            onScanComplete(!isHooked && isIntegrityValid)
        }
    }
}