# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

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

# Allow full obfuscation, optimization, and class scrambling on ViewModels and core logic
-optimizationpasses 5
-allowaccessmodification

# Suppress missing class warnings for Google Tink / ErrorProne compile-time annotations
-dontwarn com.google.errorprone.annotations.**
-dontwarn javax.annotation.**
-dontwarn org.checkerframework.**