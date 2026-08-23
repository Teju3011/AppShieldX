package com.universalapp.androidcore

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.universalapp.androidcore.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF121212)
                ) {
                    RAspshieldScreen()
                }
            }
        }
    }
}

@Composable
fun RAspshieldScreen(viewModel: MainViewModel = viewModel()) {
    val context = LocalContext.current
    val securityState by viewModel.logOutput.collectAsState()
    val isSimulating by viewModel.isSimulatingAttack.collectAsState()

    // Determine the state of the environment for visual feedback
    val isCompromised = securityState.contains("COMPROMISED") || securityState.contains("THREAT MITIGATED") || securityState.contains("true")

    val rawServerBlocked = securityState.contains("403") || securityState.contains("ENVIRONMENT_UNTRUSTED")
    val isServerBlocked = !BuildConfig.DEBUG && rawServerBlocked
    val isOffline = securityState.contains("Offline") || securityState.contains("Initial")

    // 🛑 CRITICAL CLIENT-SIDE ENFORCEMENT LOCKOUT WORKFLOW
    if (isServerBlocked) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(Color(0xFF1A0B0B))
                .padding(24.dp),
            contentAlignment = Alignment.Center
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(text = "❌", fontSize = 64.sp)
                Spacer(modifier = Modifier.height(16.dp))
                Text(
                    text = "ACCESS DENIED",
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFFEF5350)
                )
                Spacer(modifier = Modifier.height(12.dp))
                Text(
                    text = "The server rejected this device session due to a security policy violation (untrusted execution environment). Please use a secure device.",
                    fontSize = 14.sp,
                    color = Color.LightGray,
                    textAlign = TextAlign.Center,
                    lineHeight = 20.sp
                )
            }
        }
        return
    }

    val statusColor = when {
        isCompromised -> Color(0xFFEF5350) // Crimson Red for Threat
        isOffline -> Color(0xFFFFB74D)     // Amber for Idle
        else -> Color(0xFF66BB6A)          // Emerald Green for Secured
    }

    val statusTitle = when {
        isCompromised -> "ENVIRONMENT THREAT BLOCKED"
        isOffline -> "SHIELD WAITING RE-ASSESSMENT"
        else -> "SYSTEM ENVIROMENT PROTECTED"
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF0F0F12))
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(40.dp))

        Text(
            text = "AppShieldX Core",
            fontSize = 32.sp,
            fontWeight = FontWeight.ExtraBold,
            color = Color.White,
            letterSpacing = (-0.5).sp
        )
        Text(
            text = "Active Runtime Application Self-Protection",
            fontSize = 12.sp,
            color = Color.Gray,
            modifier = Modifier.padding(top = 4.dp, bottom = 36.dp)
        )

        // Status Circle Banner
        Card(
            shape = RoundedCornerShape(100.dp),
            colors = CardDefaults.cardColors(containerColor = statusColor.copy(alpha = 0.12f)),
            modifier = Modifier.size(130.dp),
            border = androidx.compose.foundation.BorderStroke(2.dp, statusColor)
        ) {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = if (isCompromised) "⚠️" else if (isOffline) "⚡" else "🛡️",
                    fontSize = 44.sp
                )
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        Text(
            text = statusTitle,
            fontWeight = FontWeight.Bold,
            fontSize = 15.sp,
            color = statusColor,
            letterSpacing = 1.sp
        )

        Spacer(modifier = Modifier.height(28.dp))

        // Logs Output Box
        Text(
            text = "DEVICE METRICS TELEMETRY LOGS",
            fontSize = 11.sp,
            color = Color.DarkGray,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.fillMaxWidth().padding(bottom = 6.dp),
            textAlign = TextAlign.Start
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .background(Color(0xFF16161E), shape = RoundedCornerShape(16.dp))
                .border(1.dp, Color(0xFF222230), shape = RoundedCornerShape(16.dp))
                .padding(20.dp)
        ) {
            Text(
                text = securityState,
                color = Color(0xFFC0CAF5),
                fontSize = 14.sp,
                fontFamily = FontFamily.Monospace,
                lineHeight = 22.sp,
                textAlign = TextAlign.Start,
                modifier = Modifier.fillMaxSize()
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Attack Simulator Toggle Button
        Button(
            onClick = { viewModel.toggleAttackSimulation() },
            colors = ButtonDefaults.buttonColors(
                containerColor = if (isSimulating) Color(0xFFD32F2F) else Color(0xFF2A2A3A)
            ),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(48.dp)
        ) {
            Text(
                text = if (isSimulating) "🔥 SIMULATING FRIDA HOOK (ACTIVE)" else "⚡ SIMULATE FRIDA HOOK ATTACK",
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold,
                color = if (isSimulating) Color.White else Color(0xFFE0E0E0)
            )
        }

        Spacer(modifier = Modifier.height(10.dp))

        // Perform Scan Action Button
        Button(
            onClick = { viewModel.performScan(context) },
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF7AA2F7)),
            shape = RoundedCornerShape(12.dp),
            modifier = Modifier
                .fillMaxWidth()
                .height(54.dp)
        ) {
            Text(
                text = "Scan Core Parameters",
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1A1B26)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))
    }
}