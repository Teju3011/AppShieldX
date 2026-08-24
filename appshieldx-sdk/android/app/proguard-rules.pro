# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.

# Preserve Jetpack Compose runtime internals so UI rendering remains intact
-keepclassmembers class * {
    @androidx.compose.runtime.Composable *;
    @androidx.compose.runtime.ReadOnlyComposable *;
}

# Keep the ThreatTelemetry data model fields intact
# so JSON keys match what the API gateway expects
-keep class com.universalapp.androidcore.model.ThreatTelemetry {
    <fields>;
}

# Preserve Native JNI Methods (Crucial for C++ NDK ptrace checks)
-keepclasseswithmembernames class * {
    native <methods>;
}

# Protect RASP Security Package from destructive renaming
-keep class com.universalapp.androidcore.security.** { *; }

# Preserve Security-Crypto & Network Dependencies
-keep class androidx.security.crypto.** { *; }
-dontwarn okhttp3.**
-dontwarn javax.annotation.**

# Allow full obfuscation, optimization, and class scrambling on ViewModels and core logic
-optimizationpasses 5
-allowaccessmodification

# Suppress missing class warnings for Google Tink / ErrorProne compile-time annotations
-dontwarn com.google.errorprone.annotations.**
-dontwarn javax.annotation.**
-dontwarn org.checkerframework.**