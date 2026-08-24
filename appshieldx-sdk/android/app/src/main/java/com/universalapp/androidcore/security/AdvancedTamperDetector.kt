package com.universalapp.androidcore.security

object AdvancedTamperDetector {

    init {
        try {
            System.loadLibrary("native-lib")
        } catch (e: UnsatisfiedLinkError) {
            // Native lib fallback handling
        }
    }

    external fun isNativeDebuggerAttached(): Boolean

    fun isHookingFrameworkPresent(): Boolean {
        val nativeCheck = try {
            isNativeDebuggerAttached()
        } catch (e: Exception) {
            false
        }
        return nativeCheck || isStackTraceHooked()
    }

    fun isStackTraceHooked(): Boolean {
        return try {
            throw Exception("RASP Stack Trace Check")
        } catch (e: Exception) {
            e.stackTrace.any { element ->
                element.className.contains("de.robv.android.xposed") ||
                        element.className.contains("com.saurik.substrate") ||
                        element.className.contains("io.frida")
            }
        }
    }
}