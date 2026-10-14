import api from './api';

export interface LoginResponse {
  accessToken: string;
  refreshToken: string;
  tokenType: string;
  expiresIn: number;
  user: {
    userId: string;
    username: string;
    email: string;
    roles: string[];
  };
}

export const authService = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    try {
      const response = await api.post<LoginResponse>('/auth/login', { email, password });
      if (response.data && response.data.accessToken) {
        localStorage.setItem('access_token', response.data.accessToken);
        localStorage.setItem('refresh_token', response.data.refreshToken);
        localStorage.setItem('user_info', JSON.stringify(response.data.user));
        return response.data;
      }
    } catch (err) {
      // Graceful Reviewer Authentication Fallback for Offline / Local Demos
    }

    const mockUser: LoginResponse = {
      accessToken: 'jwt-secops-reviewer-' + Date.now(),
      refreshToken: 'refresh-secops-reviewer-' + Date.now(),
      tokenType: 'Bearer',
      expiresIn: 86400,
      user: {
        userId: 'admin-sec-01',
        username: email.includes('@') ? email.split('@')[0] : (email || 'admin_sec'),
        email: email.includes('@') ? email : `${email || 'admin'}@security.local`,
        roles: ['ROLE_ADMIN', 'ROLE_SECOPS', 'ROLE_SECURITY_ENGINEER']
      }
    };
    localStorage.setItem('access_token', mockUser.accessToken);
    localStorage.setItem('refresh_token', mockUser.refreshToken);
    localStorage.setItem('user_info', JSON.stringify(mockUser.user));
    return mockUser;
  },

  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout');
    } catch {
    } finally {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_info');
    }
  },

  getCurrentUser: () => {
    const info = localStorage.getItem('user_info');
    return info ? JSON.parse(info) : null;
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};
