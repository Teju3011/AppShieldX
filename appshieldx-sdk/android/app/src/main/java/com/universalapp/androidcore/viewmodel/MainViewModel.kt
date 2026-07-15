package com.universalapp.androidcore.viewmodel

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import com.universalapp.androidcore.model.ThreatTelemetry
import java.io.File

class MainViewModel : ViewModel() {

    private val _securityState = MutableStateFlow("System Initialized. Awaiting Scan...")
    val securityState: StateFlow<String> = _securityState.asStateFlow()

    fun runSecurityAssessment() {
        _securityState.value = "Analyzing environment status..."
        
        // Basic static verification indicators for the device architecture environment
        val isRooted = checkRootFiles()
        val isEmulator = android.os.Build.FINGERPRINT.contains("generic") || android.os.Build.MODEL.contains("google_sdk")
        
        val telemetry = ThreatTelemetry(
            deviceId = "ANDROID_" + android.os.Build.ID,
            osVersion = android.os.Build.VERSION.RELEASE,
            isRooted = isRooted,
            isEmulator = isEmulator,
            integrityStatus = if (isRooted) "COMPROMISED" else "SECURE"
        )
        
        _securityState.value = """
            Scan Complete!
            Status: ${telemetry.integrityStatus}
            Root Detected: ${telemetry.isRooted}
            Is Emulator: ${telemetry.isEmulator}
        """.trimIndent()
    }

    private fun checkRootFiles(): Boolean {
        val paths = arrayOf(
            "/system/app/Superuser.apk",
            "/sbin/su",
            "/system/bin/su",
            "/system/xbin/su",
            "/data/local/xbin/su",
            "/data/local/bin/su",
            "/system/sd/xbin/su",
            "/system/bin/failsafe/su",
            "/data/local/su"
        )
        for (path in paths) {
            if (File(path).exists()) return true
        }
        return false
    }
}