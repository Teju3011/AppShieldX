package com.framework.security.detectors

import android.os.Build
import java.io.File

/**
 * Native Android Emulator & Virtual Environment Detection Engine.
 *
 * Inspects low-level hardware properties, QEMU communication pipes,
 * hypervisor signatures (Genymotion, VirtualBox, BlueStacks), and board metadata.
 */
class EmulatorDetector {

    companion object {
        private val QEMU_PIPES = arrayOf(
            "/dev/socket/qemud",
            "/dev/qemu_pipe",
            "/dev/socket/baseband_genyd",
            "/dev/socket/genyd"
        )
    }

    /**
     * Executes all emulator heuristic probes.
     */
    fun isEmulator(): Boolean {
        return checkBuildProperties() ||
                checkHardwareFingerprint() ||
                checkQemuPipes() ||
                checkGenymotion()
    }

    /**
     * Probe 1: Evaluates standard Build environment constants.
     */
    fun checkBuildProperties(): Boolean {
        val fingerprint = Build.FINGERPRINT.lowercase()
        val model = Build.MODEL.lowercase()
        val product = Build.PRODUCT.lowercase()
        val brand = Build.BRAND.lowercase()
        val device = Build.DEVICE.lowercase()

        return fingerprint.startsWith("generic") ||
                fingerprint.startsWith("unknown") ||
                model.contains("google_sdk") ||
                model.contains("emulator") ||
                model.contains("android sdk built for x86") ||
                model.contains("sdk_gphone") ||
                product.contains("sdk_google") ||
                product.contains("google_sdk") ||
                product.contains("sdk") ||
                product.contains("sdk_x86") ||
                product.contains("vbox86p") ||
                brand.startsWith("generic") && device.startsWith("generic")
    }

    /**
     * Probe 2: Inspects low-level hardware SoC identifiers.
     */
    fun checkHardwareFingerprint(): Boolean {
        val hardware = Build.HARDWARE.lowercase()
        val board = Build.BOARD.lowercase()

        return hardware.contains("goldfish") ||
                hardware.contains("ranchu") ||
                hardware.contains("vbox86") ||
                board.contains("goldfish") ||
                board.contains("ranchu")
    }

    /**
     * Probe 3: Detects QEMU virtualization guest-host pipe descriptors.
     */
    fun checkQemuPipes(): Boolean {
        for (path in QEMU_PIPES) {
            try {
                val file = File(path)
                if (file.exists()) {
                    return true
                }
            } catch (_: SecurityException) {
                // Denied access
            }
        }
        return false
    }

    /**
     * Probe 4: Checks for Genymotion or BlueStacks hypervisor artifacts.
     */
    fun checkGenymotion(): Boolean {
        val manufacturer = Build.MANUFACTURER.lowercase()
        val hardware = Build.HARDWARE.lowercase()
        return manufacturer.contains("genymotion") || hardware.contains("genymotion")
    }
}
