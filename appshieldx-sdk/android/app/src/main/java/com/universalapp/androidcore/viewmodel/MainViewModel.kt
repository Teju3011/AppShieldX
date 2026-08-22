package com.universalapp.androidcore.viewmodel

import android.app.Application
import android.content.pm.ApplicationInfo
import android.os.Debug
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.universalapp.androidcore.data.TelemetryDispatcher
import com.universalapp.androidcore.model.ThreatTelemetry
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.File
import java.io.FileReader
import java.net.Socket

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private val _securityState = MutableStateFlow("System Initialized. Awaiting Scan...")
    val securityState: StateFlow<String> = _securityState.asStateFlow()

    fun runSecurityAssessment() {
        _securityState.value = "Analyzing environment status..."

        viewModelScope.launch {
            val isRooted = checkRootFiles()
            val rawIsEmulator = android.os.Build.FINGERPRINT.contains("generic") || android.os.Build.MODEL.contains("google_sdk")
            val isDebuggerAttached = Debug.isDebuggerConnected() || Debug.waitingForDebugger()

            // Run the dynamic instrumentation detection vectors
            val isFridaPortActive = checkFridaDefaultPort()
            val isFridaMemoryInjected = checkFridaMemoryMaps()
            val isFridaDetected = isFridaPortActive || isFridaMemoryInjected

            // 🔒 PERMANENT FIX FOR LOCAL DEVELOPMENT:
            // Check if application is running in a Debug build environment natively.
            val isDebugBuild = (0 != (getApplication<Application>().applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE))

            // Only flag emulator as a active threat if running in a RELEASE build (!isDebugBuild).
            val isEmulator = !isDebugBuild && rawIsEmulator

            // Evaluate complete architectural integrity matrix
            val integrityStatus = if (isRooted || isEmulator || isDebuggerAttached || isFridaDetected) "COMPROMISED" else "SECURE"

            // Construct telemetry model
            val telemetry = ThreatTelemetry(
                deviceId = "ANDROID_" + android.os.Build.ID,
                osVersion = android.os.Build.VERSION.RELEASE,
                isRooted = isRooted,
                isEmulator = isEmulator,
                integrityStatus = integrityStatus
            )

            _securityState.value = "Transmitting metrics to secure gateway..."

            // Pass the application context to support EncryptedSharedPreferences (SecureStorage)
            val networkResult = TelemetryDispatcher.sendTelemetry(telemetry, getApplication())

            networkResult.onSuccess { code ->
                _securityState.value = """
                    Scan Transmitted! (HTTP $code)
                    Status: $integrityStatus
                    Root Detected: $isRooted
                    Is Emulator: $isEmulator
                    Debugger Attached: $isDebuggerAttached
                    Frida Hook Detected: $isFridaDetected
                """.trimIndent()
            }.onFailure { error ->
                _securityState.value = """
                    Scan Cached. Gateway Offline.
                    Reason: ${error.localizedMessage}
                    Status: $integrityStatus
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

    /**
     * Frida Trap 1: Scans the network stack to check if a local Frida server is active.
     */
    private suspend fun checkFridaDefaultPort(): Boolean = withContext(Dispatchers.IO) {
        try {
            // Frida server default listens on port 27042
            val socket = Socket("127.0.0.1", 27042)
            socket.close()
            true // Connection succeeded, Frida server is running!
        } catch (e: Exception) {
            false // Connection refused, port is clear
        }
    }

    /**
     * Frida Trap 2: Parses the application process memory space layout for active instrumentation agents.
     */
    private fun checkFridaMemoryMaps(): Boolean {
        try {
            val mapsFile = File("/proc/self/maps")
            if (mapsFile.exists()) {
                BufferedReader(FileReader(mapsFile)).use { reader ->
                    var line: String?
                    while (reader.readLine().also { line = it } != null) {
                        // Look for standard compiled agent library indicators or framework signatures
                        if (line?.contains("frida", ignoreCase = true) == true ||
                            line?.contains("xposed", ignoreCase = true) == true) {
                            return true
                        }
                    }
                }
            }
        } catch (e: Exception) {
            // Safe fallback if mapping system permissions vary
        }
        return false
    }
}