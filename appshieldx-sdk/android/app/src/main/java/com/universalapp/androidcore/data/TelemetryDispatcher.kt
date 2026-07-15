package com.universalapp.androidcore.data

import com.universalapp.androidcore.model.ThreatTelemetry
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

object TelemetryDispatcher {

    suspend fun sendTelemetry(telemetry: ThreatTelemetry): Result<Int> = withContext(Dispatchers.IO) {
        runCatching {
            val url = URL(ShieldNetworkConfig.telemetryEndpoint)
            val connection = url.openConnection() as HttpURLConnection
            connection.requestMethod = "POST"
            connection.setRequestProperty("Content-Type", "application/json")
            connection.doOutput = true
            connection.connectTimeout = 5000
            connection.readTimeout = 5000

            // Manually formatting data fields into a standard JSON payload string
            val jsonPayload = """
                {
                    "deviceId": "${telemetry.deviceId}",
                    "osVersion": "${telemetry.osVersion}",
                    "isRooted": ${telemetry.isRooted},
                    "isEmulator": ${telemetry.isEmulator},
                    "integrityStatus": "${telemetry.integrityStatus}",
                    "timestamp": ${telemetry.timestamp}
                }
            """.trimIndent()

            OutputStreamWriter(connection.outputStream).use { writer ->
                writer.write(jsonPayload)
                writer.flush()
            }

            val responseCode = connection.responseCode
            connection.disconnect()
            
            if (responseCode in 200..299) responseCode else throw Exception("Server returned HTTP $responseCode")
        }
    }
}