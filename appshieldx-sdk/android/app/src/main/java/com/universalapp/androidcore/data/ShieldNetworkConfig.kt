package com.universalapp.androidcore.data

object ShieldNetworkConfig {
    // 10.0.2.2 routes the Android emulator safely to your laptop's local machine gateway
    private const val GATEWAY_HOST = "http://10.0.2.2:8080"
    
    val telemetryEndpoint: String
        get() = "$GATEWAY_HOST/v1/telemetry"
        
    val checkStatusEndpoint: String
        get() = "$GATEWAY_HOST/v1/status"
}