package com.framework.security.detectors

import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test

class FridaDetectorTest {

    private lateinit var fridaDetector: FridaDetector

    @Before
    fun setUp() {
        fridaDetector = FridaDetector()
    }

    @Test
    fun testFridaDetectorInitialization() {
        assertNotNull(fridaDetector)
    }

    @Test
    fun testCheckMemoryMaps_ParsesSafely() {
        val mapsDetected = fridaDetector.checkMemoryMaps()
        assertNotNull(mapsDetected)
    }

    @Test
    fun testCheckDefaultFridaPort_RunsWithoutCrashing() {
        val portOpen = fridaDetector.checkDefaultFridaPort()
        assertNotNull(portOpen)
    }
}
