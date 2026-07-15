package com.universalapp.androidcore

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.universalapp.androidcore.ui.theme.AndroidCoreTheme
import com.universalapp.androidcore.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AndroidCoreTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    val scanStatus by viewModel.securityState.collectAsState()

                    Column(
                        modifier = Modifier
                            .fillMaxSize()
                            .padding(24.dp),
                        verticalArrangement = Arrangement.Center,
                        horizontalAlignment = Alignment.CenterHorizontally
                      ) {
                        Text(
                            text = "AppShieldX Client Toolkit",
                            fontSize = 24.sp,
                            modifier = Modifier.padding(bottom = 32.dp)
                        )
                        
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(200.dp)
                                .padding(bottom = 32.dp)
                        ) {
                            Box(
                                modifier = Modifier
                                    .fillMaxSize()
                                    .padding(16.dp),
                                contentAlignment = Alignment.TopStart
                            ) {
                                Text(
                                    text = scanStatus,
                                    fontFamily = FontFamily.Monospace,
                                    fontSize = 14.sp
                                )
                            }
                        }

                        Button(
                            onClick = { viewModel.runSecurityAssessment() },
                            modifier = Modifier.fillMaxWidth().height(50.dp)
                        ) {
                            Text("Execute Core RASP Scan")
                        }
                    }
                }
            }
        }
    }
}