package com.universalapp.androidcore.viewmodel

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import com.universalapp.androidcore.model.User

class MainViewModel : ViewModel() {

    // FIX: Added <User?> type casting so Kotlin knows this state flow holds our User model
    private val _userState = MutableStateFlow<User?>(null)

    // FIX: Added <User?> type to the public immutable StateFlow signature
    val userState: StateFlow<User?> = _userState.asStateFlow()

    fun initializeFrameworkUser() {
        _userState.value = User(
            id = "USR-779X",
            username = "Tej30_Developer",
            email = "developer@universalapp.com"
        )
    }
}