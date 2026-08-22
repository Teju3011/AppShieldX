package com.universalapp.androidcore.data

import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject

class GatewayApiService {

    // 10.0.2.2 points to localhost on your host machine from the Android Emulator
    private val BASE_URL = "http://10.0.2.2:8080"
    private val client = OkHttpClient()
    private val JSON_MEDIA = "application/json; charset=utf-8".toMediaType()

    // Step A: Request Access Token from Gateway
    fun loginDevice(deviceId: String): String? {
        val json = JSONObject().apply { put("deviceId", deviceId) }
        val body = json.toString().toRequestBody(JSON_MEDIA)

        val request = Request.Builder()
            .url("$BASE_URL/v1/auth/login")
            .post(body)
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                if (response.isSuccessful) {
                    val resObj = JSONObject(response.body?.string() ?: "")
                    resObj.optString("accessToken")
                } else null
            }
        } catch (e: Exception) {
            e.printStackTrace()
            null
        }
    }

    // Step B: Send Security Metrics with Bearer Token
    fun sendTelemetry(jwtToken: String, scanData: Map<String, Any>): Pair<Int, String> {
        val json = JSONObject(scanData)
        val body = json.toString().toRequestBody(JSON_MEDIA)

        val request = Request.Builder()
            .url("$BASE_URL/v1/telemetry")
            .addHeader("Authorization", "Bearer $jwtToken")
            .post(body)
            .build()

        return try {
            client.newCall(request).execute().use { response ->
                Pair(response.code, response.body?.string() ?: "")
            }
        } catch (e: Exception) {
            Pair(500, e.message ?: "Connection Error")
        }
    }
}