package com.framework.user.controller;

import com.framework.user.dto.UpdateUserRolesRequest;
import com.framework.user.dto.UpdateUserStatusRequest;
import com.framework.user.dto.UserAdminViewResponse;
import com.framework.user.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/admin/users")
@PreAuthorize("hasRole('ADMIN')")
public class UserAdminController {

    private final UserService userService;

    public UserAdminController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public ResponseEntity<List<UserAdminViewResponse>> listUsers() {
        return ResponseEntity.ok(userService.listAllUsers());
    }

    @PutMapping("/{userId}/status")
    public ResponseEntity<UserAdminViewResponse> updateUserStatus(
            @PathVariable UUID userId,
            @Valid @RequestBody UpdateUserStatusRequest request
    ) {
        return ResponseEntity.ok(userService.updateUserStatus(userId, request));
    }

    @PutMapping("/{userId}/roles")
    public ResponseEntity<UserAdminViewResponse> updateUserRoles(
            @PathVariable UUID userId,
            @Valid @RequestBody UpdateUserRolesRequest request
    ) {
        return ResponseEntity.ok(userService.updateUserRoles(userId, request));
    }
}
