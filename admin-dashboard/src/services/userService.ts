import api from './api';

export interface UserAdminView {
  userId: string;
  username: string;
  email: string;
  roles: string[];
  enabled: boolean;
  accountLocked: boolean;
  createdAt: string;
  updatedAt: string;
}

export const userService = {
  listUsers: async (): Promise<UserAdminView[]> => {
    const response = await api.get<UserAdminView[]>('/admin/users');
    return response.data;
  },

  updateUserStatus: async (userId: string, enabled: boolean, accountLocked: boolean): Promise<UserAdminView> => {
    const response = await api.put<UserAdminView>(`/admin/users/${userId}/status`, {
      enabled,
      accountLocked,
    });
    return response.data;
  },

  updateUserRoles: async (userId: string, roles: string[]): Promise<UserAdminView> => {
    const response = await api.put<UserAdminView>(`/admin/users/${userId}/roles`, {
      roles,
    });
    return response.data;
  },
};
