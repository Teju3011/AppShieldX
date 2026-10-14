package com.framework.security.detectors

import android.content.Context
import android.content.pm.PackageManager
import android.os.Build
import java.io.BufferedReader
import java.io.File
import java.io.InputStreamReader

/**
 * Native Android Root Detection Engine.
 *
 * Implements heuristic and signature-based probes inspecting su binaries,
 * root management applications, build tags, and filesystem mount permissions.
 */
class RootDetector(private val context: Context) {

    companion object {
        private val SU_PATHS = arrayOf(
            "/system/app/Superuser.apk",
            "/sbin/su",
            "/system/bin/su",
            "/system/xbin/su",
            "/data/local/xbin/su",
            "/data/local/bin/su",
            "/system/sd/xbin/su",
            "/system/bin/failsafe/su",
            "/data/local/su",
            "/su/bin/su"
        )

        private val KNOWN_ROOT_PACKAGES = arrayOf(
            "com.noshufou.android.su",
            "com.noshufou.android.su.elite",
            "eu.chainfire.supersu",
            "com.koushikdutta.superuser",
            "com.thirdparty.superuser",
            "com.yellowes.su",
            "com.topjohnwu.magisk",
            "com.kingroot.kinguser",
            "com.kingo.root"
        )
    }

    /**
     * Executes all root detection heuristics and returns true if any probe indicates compromise.
     */
    fun isRooted(): Boolean {
        return checkBuildTags() ||
                checkSuBinaryExistence() ||
                checkRootPackages() ||
                checkSuExecution() ||
                checkReadWriteMounts()
    }

    /**
     * Probe 1: Inspects Build.TAGS for developer/test-keys signatures.
     */
    fun checkBuildTags(): Boolean {
        val buildTags = Build.TAGS
        return buildTags != null && buildTags.contains("test-keys")
    }

    /**
     * Probe 2: Verifies physical existence of su binaries on standard filesystem partitions.
     */
    fun checkSuBinaryExistence(): Boolean {
        for (path in SU_PATHS) {
            try {
                val file = File(path)
                if (file.exists() && file.canExecute()) {
                    return true
                }
            } catch (_: SecurityException) {
                // Denied access suggests restricted permissions
            }
        }
        return false
    }

    /**
     * Probe 3: Checks if known root management packages (Magisk, SuperSU) are installed.
     */
    fun checkRootPackages(): Boolean {
        val packageManager = context.packageManager
        for (pkgName in KNOWN_ROOT_PACKAGES) {
            try {
                packageManager.getPackageInfo(pkgName, 0)
                return true
            } catch (_: PackageManager.NameNotFoundException) {
                // Not present
            }
        }
        return false
    }

    /**
     * Probe 4: Attempts to execute the su binary via Runtime.getRuntime().
     */
    fun checkSuExecution(): Boolean {
        var process: Process? = null
        return try {
            process = Runtime.getRuntime().exec(arrayOf("which", "su"))
            val reader = BufferedReader(InputStreamReader(process.inputStream))
            val line = reader.readLine()
            line != null && line.isNotEmpty()
        } catch (_: Exception) {
            false
        } finally {
            process?.destroy()
        }
    }

    /**
     * Probe 5: Inspects mount points to determine if /system or /vendor is mounted read-write (rw).
     */
    fun checkReadWriteMounts(): Boolean {
        val mountsFile = File("/proc/mounts")
        if (!mountsFile.exists() || !mountsFile.canRead()) return false

        return try {
            mountsFile.forEachLine { line ->
                val tokens = line.split(" ")
                if (tokens.size >= 4) {
                    val mountPoint = tokens[1]
                    val mountOptions = tokens[3]
                    if (mountPoint == "/system" || mountPoint == "/") {
                        val flags = mountOptions.split(",")
                        if (flags.contains("rw")) {
                            return@forEachLine
                        }
                    }
                }
            }
            false
        } catch (_: Exception) {
            false
        }
    }
}
