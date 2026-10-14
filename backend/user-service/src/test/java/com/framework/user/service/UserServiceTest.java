package com.framework.user.service;

import com.framework.user.dto.*;
import com.framework.user.entity.Role;
import com.framework.user.entity.User;
import com.framework.user.repository.RoleRepository;
import com.framework.user.repository.UserRepository;
import com.framework.user.service.impl.UserServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.server.ResponseStatusException;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("UserService Unit Tests")
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private RoleRepository roleRepository;

    @Mock
    private PasswordEncoder passwordEncoder;

    private UserServiceImpl userService;

    private User sampleUser;
    private UUID userId;
    private Role roleUser;
    private Role roleAdmin;

    @BeforeEach
    void setUp() {
        userService = new UserServiceImpl(userRepository, roleRepository, passwordEncoder);

        userId = UUID.randomUUID();
        roleUser = new Role("ROLE_USER", "Standard User");
        roleAdmin = new Role("ROLE_ADMIN", "Administrator");

        sampleUser = new User("johndoe", "john@enterprise.internal", "$2a$12$hashedPassword");
        sampleUser.setId(userId);
        sampleUser.getRoles().add(roleUser);
    }

    @Test
    @DisplayName("Should return user profile for existing user")
    void testGetUserProfileSuccess() {
        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));

        UserProfileResponse profile = userService.getUserProfile(userId);

        assertNotNull(profile);
        assertEquals(userId, profile.userId());
        assertEquals("johndoe", profile.username());
        assertEquals("john@enterprise.internal", profile.email());
        assertTrue(profile.roles().contains("ROLE_USER"));
    }

    @Test
    @DisplayName("Should update user profile if email and username are available")
    void testUpdateProfileSuccess() {
        UpdateProfileRequest request = new UpdateProfileRequest("john_updated", "new_email@enterprise.internal");

        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));
        when(userRepository.existsByEmail("new_email@enterprise.internal")).thenReturn(false);
        when(userRepository.existsByUsername("john_updated")).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);

        UserProfileResponse response = userService.updateProfile(userId, request);

        assertNotNull(response);
        assertEquals("john_updated", response.username());
        assertEquals("new_email@enterprise.internal", response.email());
        verify(userRepository, times(1)).save(sampleUser);
    }

    @Test
    @DisplayName("Should successfully change password when current password matches")
    void testChangePasswordSuccess() {
        ChangePasswordRequest request = new ChangePasswordRequest(
                "CurrentP@ss1",
                "NewSecureP@ssw0rd2026!",
                "NewSecureP@ssw0rd2026!"
        );

        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));
        when(passwordEncoder.matches("CurrentP@ss1", sampleUser.getPasswordHash())).thenReturn(true);
        when(passwordEncoder.matches("NewSecureP@ssw0rd2026!", sampleUser.getPasswordHash())).thenReturn(false);
        when(passwordEncoder.encode("NewSecureP@ssw0rd2026!")).thenReturn("new_hash");

        assertDoesNotThrow(() -> userService.changePassword(userId, request));
        verify(userRepository, times(1)).save(sampleUser);
    }

    @Test
    @DisplayName("Should reject password change if current password is wrong")
    void testChangePasswordWrongCurrent() {
        ChangePasswordRequest request = new ChangePasswordRequest(
                "WrongCurrentP@ss",
                "NewSecureP@ssw0rd2026!",
                "NewSecureP@ssw0rd2026!"
        );

        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));
        when(passwordEncoder.matches("WrongCurrentP@ss", sampleUser.getPasswordHash())).thenReturn(false);

        assertThrows(ResponseStatusException.class, () -> userService.changePassword(userId, request));
        verify(userRepository, never()).save(any(User.class));
    }

    @Test
    @DisplayName("Should update user roles for administrator")
    void testUpdateUserRolesSuccess() {
        UpdateUserRolesRequest request = new UpdateUserRolesRequest(Set.of("ROLE_USER", "ROLE_ADMIN"));

        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));
        when(roleRepository.findByName("ROLE_USER")).thenReturn(Optional.of(roleUser));
        when(roleRepository.findByName("ROLE_ADMIN")).thenReturn(Optional.of(roleAdmin));
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);

        UserAdminViewResponse response = userService.updateUserRoles(userId, request);

        assertNotNull(response);
        verify(userRepository, times(1)).save(sampleUser);
    }

    @Test
    @DisplayName("Should update user enabled and locked status")
    void testUpdateUserStatusSuccess() {
        UpdateUserStatusRequest request = new UpdateUserStatusRequest(false, true);

        when(userRepository.findById(userId)).thenReturn(Optional.of(sampleUser));
        when(userRepository.save(any(User.class))).thenReturn(sampleUser);

        UserAdminViewResponse response = userService.updateUserStatus(userId, request);

        assertNotNull(response);
        assertFalse(sampleUser.isEnabled());
        assertTrue(sampleUser.isAccountLocked());
        verify(userRepository, times(1)).save(sampleUser);
    }
}
