package com.framework.security.channel

import android.content.Context
import com.framework.security.detectors.DebuggerDetector
import com.framework.security.detectors.EmulatorDetector
import com.framework.security.detectors.FridaDetector
import com.framework.security.detectors.IntegrityChecker
import com.framework.security.detectors.RootDetector
import io.flutter.plugin.common.MethodCall
import io.flutter.plugin.common.MethodChannel
import java.time.Instant

/**
 * MethodChannel handler connecting Flutter runtime security queries
 * with native Kotlin heuristic RASP detectors.
 */
class RuntimeProtectionMethodChannelHandler(private val context: Context) : MethodChannel.MethodCallHandler {

    private val rootDetector = RootDetector(context)
    private val emulatorDetector = EmulatorDetector()
    private val debuggerDetector = DebuggerDetector(context)
    private val fridaDetector = FridaDetector()
    private val integrityChecker = IntegrityChecker(context)

    override fun onMethodCall(call: MethodCall, result: MethodChannel.Result) {
        when (call.method) {
            "checkRootOrJailbreak" -> {
                result.success(rootDetector.isRooted())
            }
            "checkEmulatorOrSimulator" -> {
                result.success(emulatorDetector.isEmulator())
            }
            "checkDebuggerAttached" -> {
                result.success(debuggerDetector.isDebuggerAttached())
            }
            "checkFrida" -> {
                result.success(fridaDetector.isFridaPresent())
            }
            "verifyIntegrity" -> {
                val expectedSignature: String? = call.argument("expectedSignature")
                result.success(integrityChecker.verifySignature(expectedSignature))
            }
            "getComprehensiveStatus" -> {
                val isRooted = rootDetector.isRooted()
                val isEmulator = emulatorDetector.isEmulator()
                val isDebugger = debuggerDetector.isDebuggerAttached()
                val isFrida = fridaDetector.isFridaPresent()
                val isIntegrityValid = integrityChecker.verifySignature(null)

                val threats = mutableListOf<String>()
                if (isRooted) threats.add("ROOT_DETECTED")
                if (isEmulator) threats.add("EMULATOR_DETECTED")
                if (isDebugger) threats.add("DEBUGGER_DETECTED")
                if (isFrida) threats.add("FRIDA_DETECTED")
                if (!isIntegrityValid) threats.add("INTEGRITY_FAILURE")

                val statusMap = mapOf<String, Any>(
                    "rootDetected" to isRooted,
                    "jailbreakDetected" to false,
                    "emulatorDetected" to isEmulator,
                    "simulatorDetected" to false,
                    "debuggerDetected" to isDebugger,
                    "fridaDetected" to isFrida,
                    "integrityValid" to isIntegrityValid,
                    "sslPinningEnabled" to true,
                    "secureStorageAvailable" to true,
                    "detectedThreats" to threats,
                    "platform" to "android",
                    "timestamp" to Instant.now().toString()
                )

                result.success(statusMap)
            }
            else -> {
                result.notImplemented()
            }
        }
    }
}
