package com.framework.user.service;

import com.framework.user.dto.*;

import java.util.List;
import java.util.UUID;

public interface UserService {

    UserProfileResponse getUserProfile(UUID userId);

    UserProfileResponse updateProfile(UUID userId, UpdateProfileRequest request);

    void changePassword(UUID userId, ChangePasswordRequest request);

    List<UserAdminViewResponse> listAllUsers();

    UserAdminViewResponse updateUserStatus(UUID userId, UpdateUserStatusRequest request);

    UserAdminViewResponse updateUserRoles(UUID userId, UpdateUserRolesRequest request);
}
