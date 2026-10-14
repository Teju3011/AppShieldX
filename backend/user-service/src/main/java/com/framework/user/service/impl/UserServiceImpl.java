package com.framework.user.service.impl;

import com.framework.user.dto.*;
import com.framework.user.entity.Role;
import com.framework.user.entity.User;
import com.framework.user.repository.RoleRepository;
import com.framework.user.repository.UserRepository;
import com.framework.user.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.*;

@Service
public class UserServiceImpl implements UserService {

    private static final Logger log = LoggerFactory.getLogger(UserServiceImpl.class);

    private final UserRepository userRepository;
    private final RoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public UserServiceImpl(
            UserRepository userRepository,
            RoleRepository roleRepository,
            PasswordEncoder passwordEncoder
    ) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional(readOnly = true)
    public UserProfileResponse getUserProfile(UUID userId) {
        User user = findUserOrThrow(userId);
        return mapToProfileResponse(user);
    }

    @Override
    @Transactional
    public UserProfileResponse updateProfile(UUID userId, UpdateProfileRequest request) {
        User user = findUserOrThrow(userId);

        String trimmedEmail = request.email().trim();
        String trimmedUsername = request.username().trim();

        if (!user.getEmail().equalsIgnoreCase(trimmedEmail) && userRepository.existsByEmail(trimmedEmail)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Email is already registered by another user");
        }

        if (!user.getUsername().equalsIgnoreCase(trimmedUsername) && userRepository.existsByUsername(trimmedUsername)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Username is already taken by another user");
        }

        user.setUsername(trimmedUsername);
        user.setEmail(trimmedEmail);
        User saved = userRepository.save(user);

        log.info("Profile updated for userId: {}", userId);
        return mapToProfileResponse(saved);
    }

    @Override
    @Transactional
    public void changePassword(UUID userId, ChangePasswordRequest request) {
        User user = findUserOrThrow(userId);

        if (!passwordEncoder.matches(request.currentPassword(), user.getPasswordHash())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Current password is incorrect");
        }

        if (!request.newPassword().equals(request.confirmPassword())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "New password and confirmation password do not match");
        }

        if (passwordEncoder.matches(request.newPassword(), user.getPasswordHash())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "New password cannot be identical to current password");
        }

        user.setPasswordHash(passwordEncoder.encode(request.newPassword()));
        userRepository.save(user);
        log.info("Password successfully changed for userId: {}", userId);
    }

    @Override
    @Transactional(readOnly = true)
    public List<UserAdminViewResponse> listAllUsers() {
        return userRepository.findAll().stream()
                .map(this::mapToAdminResponse)
                .toList();
    }

    @Override
    @Transactional
    public UserAdminViewResponse updateUserStatus(UUID userId, UpdateUserStatusRequest request) {
        User user = findUserOrThrow(userId);

        user.setEnabled(request.enabled());
        user.setAccountLocked(request.accountLocked());
        User saved = userRepository.save(user);

        log.info("User status updated for userId: {} [enabled={}, accountLocked={}]",
                userId, request.enabled(), request.accountLocked());
        return mapToAdminResponse(saved);
    }

    @Override
    @Transactional
    public UserAdminViewResponse updateUserRoles(UUID userId, UpdateUserRolesRequest request) {
        User user = findUserOrThrow(userId);

        Set<Role> newRoles = new HashSet<>();
        for (String roleName : request.roles()) {
            String canonicalName = roleName.startsWith("ROLE_") ? roleName : "ROLE_" + roleName;
            Role role = roleRepository.findByName(canonicalName)
                    .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid role name: " + roleName));
            newRoles.add(role);
        }

        user.setRoles(newRoles);
        User saved = userRepository.save(user);

        log.info("Roles updated for userId: {} [roles={}]", userId, request.roles());
        return mapToAdminResponse(saved);
    }

    private User findUserOrThrow(UUID userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found"));
    }

    private UserProfileResponse mapToProfileResponse(User user) {
        List<String> roles = user.getRoles().stream()
                .map(Role::getName)
                .toList();

        return new UserProfileResponse(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                roles,
                user.isEnabled(),
                user.isAccountLocked(),
                user.getCreatedAt(),
                user.getUpdatedAt()
        );
    }

    private UserAdminViewResponse mapToAdminResponse(User user) {
        List<String> roles = user.getRoles().stream()
                .map(Role::getName)
                .toList();

        return new UserAdminViewResponse(
                user.getId(),
                user.getUsername(),
                user.getEmail(),
                roles,
                user.isEnabled(),
                user.isAccountLocked(),
                user.getCreatedAt(),
                user.getUpdatedAt()
        );
    }
}
