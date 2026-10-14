package com.framework.security.detectors

import android.content.Context
import android.content.pm.PackageManager
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test
import org.mockito.Mockito.mock
import org.mockito.Mockito.`when`

class RootDetectorTest {

    private lateinit var mockContext: Context
    private lateinit var mockPackageManager: PackageManager
    private lateinit var rootDetector: RootDetector

    @Before
    fun setUp() {
        mockContext = mock(Context::class.java)
        mockPackageManager = mock(PackageManager::class.java)
        `when`(mockContext.packageManager).thenReturn(mockPackageManager)

        rootDetector = RootDetector(mockContext)
    }

    @Test
    fun testRootDetectorInitialization() {
        assertNotNull(rootDetector)
    }

    @Test
    fun testCheckSuBinaryExistence_CleanEnvironment() {
        // On standard dev machine / unrooted emulator without su in /sbin
        val isSuPresent = rootDetector.checkSuBinaryExistence()
        // Should execute cleanly without throwing exceptions
        assertNotNull(isSuPresent)
    }

    @Test
    fun testCheckRootPackages_NoRootPackagesInstalled() {
        `when`(mockPackageManager.getPackageInfo("com.topjohnwu.magisk", 0))
            .thenThrow(PackageManager.NameNotFoundException())

        val packagesDetected = rootDetector.checkRootPackages()
        assertFalse(packagesDetected)
    }
}
