package com.framework.security.storage

import android.content.Context
import android.content.SharedPreferences
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

/**
 * Native Android Hardware-Backed Secure Key-Value Storage.
 *
 * Utilizes Jetpack Security MasterKey generated inside the AndroidKeyStore
 * with AES-256-GCM encrypted SharedPreferences for sensitive credentials.
 */
class AndroidSecureStorage(context: Context) {

    private val sharedPreferences: SharedPreferences

    init {
        val masterKey = MasterKey.Builder(context)
            .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
            .setRequestStrongBoxBacked(false) // Fall back gracefully if StrongBox HSM chip absent
            .build()

        sharedPreferences = EncryptedSharedPreferences.create(
            context,
            "cloud_native_sec_prefs",
            masterKey,
            EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
            EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
        )
    }

    fun write(key: String, value: String) {
        sharedPreferences.edit().putString(key, value).apply()
    }

    fun read(key: String): String? {
        return sharedPreferences.getString(key, null)
    }

    fun delete(key: String) {
        sharedPreferences.edit().remove(key).apply()
    }

    fun contains(key: String): Boolean {
        return sharedPreferences.contains(key)
    }

    fun clear() {
        sharedPreferences.edit().clear().apply()
    }
}
