package com.universalapp.androidcore.security

import android.content.Context
import android.os.Handler
import android.os.Looper
import android.widget.Toast

object ThreatMitigationHandler {

    enum class ThreatLevel {
        LOW, MEDIUM, HIGH, CRITICAL
    }

    fun handleDetectedThreat(context: Context, threatName: String, level: ThreatLevel) {
        val storage = SecureStorageManager(context)

        // Ensure UI operations execute on the Main Thread
        Handler(Looper.getMainLooper()).post {
            when (level) {
                ThreatLevel.CRITICAL -> {
                    // Instantly wipe access tokens and local storage
                    storage.clearStorage()
                    Toast.makeText(context, "CRITICAL THREAT: $threatName. Session Terminated.", Toast.LENGTH_LONG).show()
                }
                ThreatLevel.HIGH -> {
                    Toast.makeText(context, "WARNING: $threatName detected.", Toast.LENGTH_SHORT).show()
                }
                else -> {
                    // Log silently
                }
            }
        }
    }
}