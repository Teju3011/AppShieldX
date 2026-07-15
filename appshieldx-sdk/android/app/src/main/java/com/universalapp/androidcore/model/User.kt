package com.universalapp.androidcore.model

/**
 * Clean data model representing a core system user.
 * This structure is entirely decoupled from the UI layers.
 */
data class User(
    val id: String,
    val username: String,
    val email: String,
    val isActive: Boolean = true
)