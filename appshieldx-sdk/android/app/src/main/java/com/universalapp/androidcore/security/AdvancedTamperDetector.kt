package com.universalapp.androidcore.security

import java.io.File

object AdvancedTamperDetector {
    fun isHookingFrameworkPresent(): Boolean {
        val suspiciousPaths = arrayOf(
            "/system/framework/XposedBridge.jar",
            "/system/lib/libxposed_art.so",
            "/data/local/tmp/frida-server",
            "/data/local/tmp/re.frida.server"
        )
        for (path in suspiciousPaths) {
            if (File(path).exists()) return true
        }
        return false
    }

    fun isStackTraceHooked(): Boolean {
        try {
            throw Exception("Check Trace")
        } catch (e: Exception) {
            for (element in e.stackTrace) {
                if (element.className.contains("de.robv.android.xposed") ||
                    element.className.contains("com.saurik.substrate") ||
                    element.className.contains("io.frida")) {
                    return true
                }
            }
        }
        return false
    }
}