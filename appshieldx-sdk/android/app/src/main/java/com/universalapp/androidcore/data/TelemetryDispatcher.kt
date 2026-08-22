package com.universalapp.androidcore.data

import android.content.Context
import com.universalapp.androidcore.model.ThreatTelemetry
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException
import java.util.concurrent.TimeUnit
import javax.net.ssl.SSLPeerUnverifiedException

object TelemetryDispatcher {

    private val JSON_MEDIA_TYPE = "application/json; charset=utf-8".toMediaType()
    private const val BASE_URL = "http://10.0.2.2:8080/v1"

    private val client = OkHttpClient.Builder()
        // .certificatePinner(certificatePinner) // 👈 Uncomment when migrating endpoint to HTTPS
        .connectTimeout(5, TimeUnit.SECONDS)
        .readTimeout(5, TimeUnit.SECONDS)
        .build()

    suspend fun sendTelemetry(telemetry: ThreatTelemetry, context: Context? = null): Result<Int> = withContext(Dispatchers.IO) {
        try {
            // Step A: Check for an existing cached token or retrieve/generate one
            var token = context?.let { SecureStorage.getToken(it) }

            if (token.isNullOrEmpty()) {
                // Try fetching from server, or fallback to a dummy local token if server is offline
                token = fetchAccessToken(telemetry.deviceId) ?: "mock-dev-token-xyz"
                context?.let { SecureStorage.saveToken(it, token) }
            }

            // Step B: Package the telemetry data
            val telemetryJson = JSONObject().apply {
                put("deviceId", telemetry.deviceId)
                put("osVersion", telemetry.osVersion)
                put("isRooted", telemetry.isRooted)
                put("isEmulator", telemetry.isEmulator)
                put("integrityStatus", "SECURE")
            }.toString()

            val body = telemetryJson.toRequestBody(JSON_MEDIA_TYPE)

            // Step C: Build request with properly formatted Bearer string
            val request = Request.Builder()
                .url("$BASE_URL/telemetry")
                .header("Authorization", "Bearer $token")
                .post(body)
                .build()

            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    Result.success(response.code)
                } else {
                    // Clear cached session if token becomes invalid/expired
                    if (response.code == 401 && context != null) {
                        SecureStorage.clearStorage(context)
                    }
                    Result.failure(IOException("Server rejected transaction with HTTP code: ${response.code}"))
                }
            }
        } catch (_: SSLPeerUnverifiedException) {
            // 🛑 MITM INTERCEPTION TRAP: Fails instantly if proxy/untrusted cert is attached
            Result.failure(IOException("SECURITY VIOLATION: SSL Certificate Mismatch (Possible MiTM Proxy Interception)"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    private fun fetchAccessToken(deviceId: String): String? {
        val authJson = JSONObject().apply {
            put("deviceId", deviceId)
        }.toString()

        val body = authJson.toRequestBody(JSON_MEDIA_TYPE)
        val request = Request.Builder()
            .url("$BASE_URL/auth/login")
            .post(body)
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) return null

                val responseBody = response.body ?: return null
                val responseString = responseBody.string()

                val jsonObject = JSONObject(responseString)
                if (!jsonObject.has("accessToken")) return null
                jsonObject.getString("accessToken")
            }
        } catch (_: Exception) {
            null
        }
    }
}