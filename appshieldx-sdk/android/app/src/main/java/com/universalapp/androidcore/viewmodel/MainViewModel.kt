package com.universalapp.androidcore.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import com.universalapp.androidcore.model.ThreatTelemetry
import com.universalapp.androidcore.data.TelemetryDispatcher
import java.io.File

class MainViewModel : ViewModel() {

    private val _securityState = MutableStateFlow("System Initialized. Awaiting Scan...")
    val securityState: StateFlow<String> = _securityState.asStateFlow()

    fun runSecurityAssessment() {
        _securityState.value = "Analyzing environment status..."
        
        val isRooted = checkRootFiles()
        val isEmulator = android.os.Build.FINGERPRINT.contains("generic") || android.os.Build.MODEL.contains("google_sdk")
        
        val telemetry = ThreatTelemetry(
            deviceId = "ANDROID_" + android.os.Build.ID,
            osVersion = android.os.Build.VERSION.RELEASE,
            isRooted = isRooted,
            isEmulator = isEmulator,
            integrityStatus = if (isRooted) "COMPROMISED" else "SECURE"
        )
        
        // Launch a coroutine to push telemetry off the main UI thread
        viewModelScope.launch {
            _securityState.value = "Transmitting metrics to secure gateway..."
            val networkResult = TelemetryDispatcher.sendTelemetry(telemetry)
            
            networkResult.onSuccess { code ->
                _securityState.value = """
                    Scan Transmitted! (HTTP $code)
                    Status: ${telemetry.integrityStatus}
                    Root Detected: ${telemetry.isRooted}
                    Is Emulator: ${telemetry.isEmulator}
                """.trimIndent()
            }.onFailure { error ->
                _securityState.value = """
                    Scan Cached. Gateway Offline.
                    Reason: ${error.localizedMessage}
                    Status: ${telemetry.integrityStatus}
                """.trimIndent()
            }
        }
    }

    private fun checkRootFiles(): Boolean {
        val paths = arrayOf("/system/app/Superuser.apk", "/sbin/su", "/system/bin/su", "/system/xbin/su")
        for (path in paths) {
            if (File(path).exists()) return true
        }
        return false
    }
}