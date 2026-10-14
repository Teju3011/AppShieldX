package com.framework.security.network

import java.security.MessageDigest
import java.security.cert.CertificateException
import java.security.cert.X509Certificate

/**
 * Native Android Certificate & Public Key Pinning Manager.
 *
 * Enforces Subject Public Key Info (SPKI) SHA-256 verification against untrusted TLS proxies.
 */
class CertificatePinningManager(private val pinnedHashes: List<String>) {

    /**
     * Validates that at least one certificate in the presented X.509 chain
     * matches the configured SHA-256 SPKI pinned fingerprints.
     */
    fun verifyCertificateChain(chain: Array<X509Certificate>?, hostname: String): Boolean {
        if (pinnedHashes.isEmpty()) return true
        if (chain.isNullOrEmpty()) return false

        val md = MessageDigest.getInstance("SHA-256")

        for (cert in chain) {
            val spkiBytes = cert.publicKey.encoded
            val sha256Digest = md.digest(spkiBytes)
            val spkiHex = sha256Digest.joinToString("") { "%02X".format(it) }

            for (pinned in pinnedHashes) {
                val cleanPin = pinned.replace("sha256/", "").replace(":", "").uppercase()
                if (cleanPin == spkiHex) {
                    return true // Pin matched
                }
            }
        }

        return false // No certificates in the presented chain matched the pinned SPKI
    }
}
