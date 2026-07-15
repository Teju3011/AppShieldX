package com.universalapp.androidcore

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.universalapp.androidcore.ui.theme.AndroidcoreTheme
import com.universalapp.androidcore.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        // Directly instantiate our fixed framework viewmodel
        val viewModel = MainViewModel()

        setContent {
            AndroidcoreTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    FrameworkStatusScreen(
                        viewModel = viewModel,
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun FrameworkStatusScreen(viewModel: MainViewModel, modifier: Modifier = Modifier) {
    // Collect the framework state changes reactively
    val user by viewModel.userState.collectAsState()

    Column(
        modifier = modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        if (user == null) {
            Text(
                text = "Android Core Framework: Ready",
                style = MaterialTheme.typography.headlineSmall
            )
            Spacer(modifier = Modifier.height(16.dp))
            Button(onClick = { viewModel.initializeFrameworkUser() }) {
                Text("Load Framework Model")
            }
        } else {
            Card(
                modifier = Modifier.fillMaxWidth().padding(16.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = "Model Loaded Successfully!",
                        style = MaterialTheme.typography.titleMedium
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(text = "ID: ${user?.id}")
                    Text(text = "User: ${user?.username}")
                    Text(text = "Email: ${user?.email}")
                }
            }
        }
    }
}