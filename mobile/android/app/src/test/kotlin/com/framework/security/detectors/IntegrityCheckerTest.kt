package com.framework.security.detectors

import android.content.Context
import android.content.pm.PackageManager
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test
import org.mockito.Mockito.mock
import org.mockito.Mockito.`when`

class IntegrityCheckerTest {

    private lateinit var mockContext: Context
    private lateinit var mockPackageManager: PackageManager
    private lateinit var integrityChecker: IntegrityChecker

    @Before
    fun setUp() {
        mockContext = mock(Context::class.java)
        mockPackageManager = mock(PackageManager::class.java)
        `when`(mockContext.packageManager).thenReturn(mockPackageManager)
        `when`(mockContext.packageName).thenReturn("com.framework.security")

        integrityChecker = IntegrityChecker(mockContext)
    }

    @Test
    fun testIntegrityCheckerInitialization() {
        assertNotNull(integrityChecker)
    }

    @Test
    fun testVerifySignature_ReturnsFalseOnMissingSignatures() {
        // Without mocked valid signature array, method returns false safely
        val isValid = integrityChecker.verifySignature("NON_MATCHING_SHA256_HASH")
        assertFalse(isValid)
    }
}
