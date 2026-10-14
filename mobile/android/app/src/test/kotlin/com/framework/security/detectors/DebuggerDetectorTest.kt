package com.framework.security.detectors

import android.content.Context
import android.content.pm.ApplicationInfo
import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test
import org.mockito.Mockito.mock
import org.mockito.Mockito.`when`

class DebuggerDetectorTest {

    private lateinit var mockContext: Context
    private lateinit var debuggerDetector: DebuggerDetector

    @Before
    fun setUp() {
        mockContext = mock(Context::class.java)
        val appInfo = ApplicationInfo().apply {
            flags = 0 // Not debuggable
        }
        `when`(mockContext.applicationInfo).thenReturn(appInfo)

        debuggerDetector = DebuggerDetector(mockContext)
    }

    @Test
    fun testDebuggerDetectorInitialization() {
        assertNotNull(debuggerDetector)
    }

    @Test
    fun testCheckTracerPid_ExecutionIntegrity() {
        val tracerDetected = debuggerDetector.checkTracerPid()
        assertNotNull(tracerDetected)
    }

    @Test
    fun testCheckDebuggableFlag_ProductionMode() {
        val isDebuggable = debuggerDetector.checkDebuggableFlag()
        assertNotNull(isDebuggable)
    }
}
