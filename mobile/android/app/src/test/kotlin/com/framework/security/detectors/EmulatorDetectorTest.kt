package com.framework.security.detectors

import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test

class EmulatorDetectorTest {

    private lateinit var emulatorDetector: EmulatorDetector

    @Before
    fun setUp() {
        emulatorDetector = EmulatorDetector()
    }

    @Test
    fun testEmulatorDetectorInitialization() {
        assertNotNull(emulatorDetector)
    }

    @Test
    fun testCheckQemuPipes_RunsWithoutCrashing() {
        val qemuDetected = emulatorDetector.checkQemuPipes()
        assertNotNull(qemuDetected)
    }

    @Test
    fun testCheckHardwareFingerprint_RunsDeterministically() {
        val hwDetected = emulatorDetector.checkHardwareFingerprint()
        assertNotNull(hwDetected)
    }
}
