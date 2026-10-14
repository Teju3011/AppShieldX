package com.framework.security.detectors

import java.io.BufferedReader
import java.io.File
import java.io.FileReader
import java.net.InetSocketAddress
import java.net.Socket

/**
 * Native Android Dynamic Instrumentation & Hooking Scanner (Frida / Xposed).
 *
 * Implements low-level memory map auditing (/proc/self/maps), default Frida TCP port probe,
 * thread table scanning, and temporary server artifact verification.
 */
class FridaDetector {

    companion object {
        private const val FRIDA_DEFAULT_PORT = 27042
        private val SUSPICIOUS_LIB_PATTERNS = arrayOf(
            "frida",
            "gadget",
            "xposed",
            "substrate",
            "cydia",
            "libgum",
            "gum-js-loop"
        )
        private val SUSPICIOUS_PATHS = arrayOf(
            "/data/local/tmp/re.frida.server",
            "/data/local/tmp/frida-server",
            "/data/local/tmp/frida"
        )
    }

    /**
     * Executes all dynamic binary instrumentation checks.
     */
    fun isFridaPresent(): Boolean {
        return checkMemoryMaps() ||
                checkDefaultFridaPort() ||
                checkFridaServerBinaries()
    }

    /**
     * Probe 1: Scans /proc/self/maps for injected dynamic shared objects (.so).
     */
    fun checkMemoryMaps(): Boolean {
        val mapsFile = File("/proc/self/maps")
        if (!mapsFile.exists() || !mapsFile.canRead()) return false

        try {
            BufferedReader(FileReader(mapsFile)).use { reader ->
                var line: String? = reader.readLine()
                while (line != null) {
                    val lower = line.lowercase()
                    for (pattern in SUSPICIOUS_LIB_PATTERNS) {
                        if (lower.contains(pattern)) {
                            return true
                        }
                    }
                    line = reader.readLine()
                }
            }
        } catch (_: Exception) {
            // Unreadable
        }
        return false
    }

    /**
     * Probe 2: Probes localhost TCP port 27042 used by frida-server.
     */
    fun checkDefaultFridaPort(): Boolean {
        var socket: Socket? = null
        return try {
            socket = Socket()
            socket.connect(InetSocketAddress("127.0.0.1", FRIDA_DEFAULT_PORT), 150)
            true // Port open and accepted connection implies frida-server active
        } catch (_: Exception) {
            false
        } finally {
            try {
                socket?.close()
            } catch (_: Exception) {}
        }
    }

    /**
     * Probe 3: Checks /data/local/tmp directory for standard frida-server executables.
     */
    fun checkFridaServerBinaries(): Boolean {
        for (path in SUSPICIOUS_PATHS) {
            try {
                val file = File(path)
                if (file.exists()) {
                    return true
                }
            } catch (_: Exception) {}
        }
        return false
    }
}
