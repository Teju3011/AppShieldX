package com.framework.security

import android.os.Bundle
import android.view.WindowManager
import com.framework.security.channel.RuntimeProtectionMethodChannelHandler
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

/**
 * Main Android Application Entry Point.
 *
 * Configures Flutter engine, attaches the native runtime security MethodChannel,
 * and enforces window security controls (FLAG_SECURE) to prevent screenshot snooping.
 */
class MainActivity : FlutterActivity() {

    companion object {
        private const val CHANNEL = "com.framework.security/runtime_protection"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        // Anti-Snooping Security Control (FLAG_SECURE):
        // Enforced for production release builds; relaxed in debug builds for demonstration screenshots.
        val isDebug = (applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0
        if (!isDebug) {
            window.setFlags(
                WindowManager.LayoutParams.FLAG_SECURE,
                WindowManager.LayoutParams.FLAG_SECURE
            )
        }
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        val channel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
        channel.setMethodCallHandler(RuntimeProtectionMethodChannelHandler(applicationContext))
    }
}
