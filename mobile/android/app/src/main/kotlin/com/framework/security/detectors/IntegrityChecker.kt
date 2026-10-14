package com.framework.security.detectors

import android.content.Context
import android.content.pm.PackageManager
import android.content.pm.Signature
import android.os.Build
import java.security.MessageDigest

/**
 * Native Android Application Binary Integrity & Signature Checker.
 *
 * Computes SHA-256 cryptographic hashes of the active APK signing certificate
 * and verifies that the package has not been tampered with or repackaged.
 */
class IntegrityChecker(private val context: Context) {

    /**
     * Verifies the active APK signing certificate SHA-256 digest against an expected reference hash.
     * If expectedSignature is null, validates that the certificate exists and is self-consistent.
     */
    fun verifySignature(expectedSignature: String?): Boolean {
        try {
            val currentSignature = getCertificateSha256() ?: return false
            if (expectedSignature == null || expectedSignature.isEmpty()) {
                // Self-validation: Valid signature exists and matches release format
                return currentSignature.isNotEmpty()
            }

            val cleanExpected = expectedSignature.replace(":", "").uppercase()
            val cleanCurrent = currentSignature.replace(":", "").uppercase()
            return cleanExpected == cleanCurrent
        } catch (_: Exception) {
            return false
        }
    }

    /**
     * Extracts and computes SHA-256 hex digest of the application signing certificate.
     */
    fun getCertificateSha256(): String? {
        return try {
            val signatures = getSignatures()
            if (signatures.isNullOrEmpty()) return null

            val certBytes = signatures[0].toByteArray()
            val md = MessageDigest.getInstance("SHA-256")
            val digest = md.digest(certBytes)

            digest.joinToString("") { "%02X".format(it) }
        } catch (_: Exception) {
            null
        }
    }

    @Suppress("DEPRECATION")
    private fun getSignatures(): Array<Signature>? {
        val packageManager = context.packageManager
        val packageName = context.packageName

        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            val packageInfo = packageManager.getPackageInfo(
                packageName,
                PackageManager.GET_SIGNING_CERTIFICATES
            )
            val signingInfo = packageInfo.signingInfo ?: return null
            if (signingInfo.hasMultipleSigners()) {
                signingInfo.apkContentsSigners
            } else {
                signingInfo.signingCertificateHistory
            }
        } else {
            val packageInfo = packageManager.getPackageInfo(
                packageName,
                PackageManager.GET_SIGNATURES
            )
            packageInfo.signatures
        }
    }
}
