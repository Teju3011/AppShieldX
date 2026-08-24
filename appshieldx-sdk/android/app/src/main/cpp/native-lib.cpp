#include <jni.h>
#include <sys/ptrace.h>
#include <unistd.h>
#include <cstdio>
#include <cstring>

extern "C" JNIEXPORT jboolean JNICALL
Java_com_universalapp_androidcore_security_AdvancedTamperDetector_isNativeDebuggerAttached(
        JNIEnv* env,
        jobject /* this */) {

    // 1. Check ptrace anti-debugging
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        return JNI_TRUE;
    }

    // 2. Parse /proc/self/maps to detect Frida/Xposed memory injections
    FILE* fp = fopen("/proc/self/maps", "r");
    if (fp != nullptr) {
        char line[512];
        while (fgets(line, sizeof(line), fp)) {
            if (strstr(line, "frida") != nullptr ||
                strstr(line, "xposed") != nullptr ||
                strstr(line, "gadget") != nullptr) {
                fclose(fp);
                return JNI_TRUE;
            }
        }
        fclose(fp);
    }

    return JNI_FALSE;
}