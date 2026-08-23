package com.universalapp.androidcore.security

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class SecureStorageManager(context: Context) {

    private val prefs: SharedPreferences = createEncryptedPreferences(context)

    private fun createEncryptedPreferences(context: Context): SharedPreferences {
        return try {
            val masterKey = MasterKey.Builder(context)
                .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
                .build()

            EncryptedSharedPreferences.create(
                context,
                "appshieldx_secure_prefs",
                masterKey,
                EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
                EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
            )
        } catch (e: Exception) {
            // Fallback to isolated SharedPreferences if API 36 / Emulator KeyStore fails
            context.getSharedPreferences("appshieldx_fallback_prefs", Context.MODE_PRIVATE)
        }
    }

    fun saveAuthToken(token: String) {
        prefs.edit().putString("KEY_JWT_TOKEN", token).apply()
    }

    fun getAuthToken(): String? {
        return prefs.getString("KEY_JWT_TOKEN", null)
    }

    fun clearStorage() {
        prefs.edit().clear().apply()
    }
}