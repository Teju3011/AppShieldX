package com.universalapp.androidcore.model

data class ThreatTelemetry(
    val deviceId: String,
    val osVersion: String,
    val isRooted: Boolean,
    val isEmulator: Boolean,
    val integrityStatus: String,
    val timestamp: Long = System.currentTimeMillis()
)