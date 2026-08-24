#include <jni.h>
#include <sys/ptrace.h>
#include <unistd.h>

extern "C" JNIEXPORT jboolean JNICALL
Java_com_universalapp_androidcore_security_AdvancedTamperDetector_isNativeDebuggerAttached(
        JNIEnv* env,
        jobject /* this */) {
    // ptrace returns -1 if a debugger or Frida native thread is actively attached
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        return JNI_TRUE;
    }
    return JNI_FALSE;
}