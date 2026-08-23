package com.universalapp.androidcore.security

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.security.MessageDigest

object SecurityIntegrityChecker {
    private const val EXPECTED_SIGNATURE_SHA256 = "YOUR_RELEASE_KEY_SHA256_HASH_HERE"

    fun verifyAppIntegrity(context: Context): Boolean {
        val currentSignature = getAppSignatureSHA256(context) ?: return false
        return currentSignature.equals(EXPECTED_SIGNATURE_SHA256, ignoreCase = true)
    }

    private fun getAppSignatureSHA256(context: Context): String? {
        return try {
            val packageManager = context.packageManager
            val packageName = context.packageName
            val signatures = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNING_CERTIFICATES).signingInfo?.apkContentsSigners
            } else {
                @Suppress("DEPRECATION")
                packageManager.getPackageInfo(packageName, PackageManager.GET_SIGNATURES).signatures
            }
            val cert = signatures?.firstOrNull()?.toByteArray() ?: return null
            val md = MessageDigest.getInstance("SHA-256")
            md.digest(cert).joinToString("") { "%02X".format(it) }
        } catch (e: Exception) {
            null
        }
    }
}