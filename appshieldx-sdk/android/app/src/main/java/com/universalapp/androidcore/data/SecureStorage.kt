package com.universalapp.androidcore.data

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

object SecureStorage {

    private const val PREF_FILE_NAME = "secure_app_prefs"
    private const val KEY_ACCESS_TOKEN = "access_token"

    private fun getEncryptedPrefs(context: Context): SharedPreferences {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .build()

        return EncryptedSharedPreferences.create(
            context,
            PREF_FILE_NAME,
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV, // 👈 Fixed enum reference
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    fun saveToken(context: Context, token: String) {
        getEncryptedPrefs(context).edit().putString(KEY_ACCESS_TOKEN, token).apply()
    }

    fun getToken(context: Context): String? {
        return getEncryptedPrefs(context).getString(KEY_ACCESS_TOKEN, null)
    }

    fun clearStorage(context: Context) {
        getEncryptedPrefs(context).edit().clear().apply()
    }
}