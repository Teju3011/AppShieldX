package com.framework.security.detectors

import android.content.Context
import android.content.pm.ApplicationInfo
import android.os.Debug
import java.io.BufferedReader
import java.io.File
import java.io.FileReader

/**
 * Native Android Debugger & Tracer Detection Engine.
 *
 * Implements low-level probes checking JDWP connections, Linux /proc/self/status TracerPid,
 * and ApplicationInfo debugging manifests.
 */
class DebuggerDetector(private val context: Context) {

    /**
     * Executes debugger detection probes.
     */
    fun isDebuggerAttached(): Boolean {
        return checkJavaDebugger() ||
                checkTracerPid() ||
                checkDebuggableFlag() ||
                checkAdbOrUsbDebugging()
    }

    /**
     * Probe 4: Checks if ADB / USB Debugging is actively enabled in Android Developer Options.
     * Matches real-world banking checks (e.g., HDFC, ICICI) by inspecting Settings.Global.ADB_ENABLED.
     */
    fun checkAdbOrUsbDebugging(): Boolean {
        return try {
            android.provider.Settings.Global.getInt(
                context.contentResolver,
                android.provider.Settings.Global.ADB_ENABLED, 0
            ) == 1
        } catch (_: Exception) {
            try {
                @Suppress("DEPRECATION")
                android.provider.Settings.Secure.getInt(
                    context.contentResolver,
                    android.provider.Settings.Secure.ADB_ENABLED, 0
                ) == 1
            } catch (_: Exception) {
                false
            }
        }
    }

    /**
     * Probe 1: Queries Android OS Debug framework for active JDWP connections.
     */
    fun checkJavaDebugger(): Boolean {
        return Debug.isDebuggerConnected() || Debug.waitingForDebugger()
    }

    /**
     * Probe 2: Reads /proc/self/status to detect active native ptrace attachments (TracerPid != 0).
     */
    fun checkTracerPid(): Boolean {
        val statusFile = File("/proc/self/status")
        if (!statusFile.exists() || !statusFile.canRead()) return false

        try {
            BufferedReader(FileReader(statusFile)).use { reader ->
                var line: String? = reader.readLine()
                while (line != null) {
                    if (line.startsWith("TracerPid:")) {
                        val pidStr = line.substring("TracerPid:".length).trim()
                        val pid = pidStr.toIntOrNull() ?: 0
                        return pid > 0
                    }
                    line = reader.readLine()
                }
            }
        } catch (_: Exception) {
            // Cannot inspect
        }
        return false
    }

    /**
     * Probe 3: Checks if the application APK manifest was compiled with android:debuggable="true".
     */
    fun checkDebuggableFlag(): Boolean {
        return (context.applicationInfo.flags and ApplicationInfo.FLAG_DEBUGGABLE) != 0
    }
}
