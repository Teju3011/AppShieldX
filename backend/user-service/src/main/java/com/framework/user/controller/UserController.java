package com.framework.user.controller;

import com.framework.user.dto.ChangePasswordRequest;
import com.framework.user.dto.MessageResponse;
import com.framework.user.dto.UpdateProfileRequest;
import com.framework.user.dto.UserProfileResponse;
import com.framework.user.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/me")
    public ResponseEntity<UserProfileResponse> getCurrentUser(Authentication authentication) {
        UUID userId = extractUserId(authentication);
        return ResponseEntity.ok(userService.getUserProfile(userId));
    }

    @PutMapping("/me")
    public ResponseEntity<UserProfileResponse> updateCurrentUser(
            Authentication authentication,
            @Valid @RequestBody UpdateProfileRequest request
    ) {
        UUID userId = extractUserId(authentication);
        return ResponseEntity.ok(userService.updateProfile(userId, request));
    }

    @PutMapping("/me/password")
    public ResponseEntity<MessageResponse> changePassword(
            Authentication authentication,
            @Valid @RequestBody ChangePasswordRequest request,
            @RequestHeader(value = "X-Correlation-ID", defaultValue = "") String correlationId
    ) {
        UUID userId = extractUserId(authentication);
        userService.changePassword(userId, request);
        return ResponseEntity.ok(MessageResponse.of("Password updated successfully", correlationId));
    }

    private UUID extractUserId(Authentication authentication) {
        return UUID.fromString(authentication.getName());
    }
}
