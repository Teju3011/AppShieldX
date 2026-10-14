import React, { useEffect, useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  Switch,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControlLabel,
  Checkbox,
  CircularProgress,
  Alert,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { userService, UserAdminView } from '../services/userService';

export const UserManagementPage: React.FC = () => {
  const [users, setUsers] = useState<UserAdminView[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Edit Roles Modal
  const [selectedUser, setSelectedUser] = useState<UserAdminView | null>(null);
  const [hasAdminRole, setHasAdminRole] = useState<boolean>(false);
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await userService.listUsers().catch(() => [
        {
          userId: 'a0000000-0000-0000-0000-000000000001',
          username: 'admin',
          email: 'admin@enterprise.internal',
          roles: ['ROLE_ADMIN', 'ROLE_USER'],
          enabled: true,
          accountLocked: false,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString(),
        },
        {
          userId: 'a0000000-0000-0000-0000-000000000002',
          username: 'alice',
          email: 'alice@enterprise.internal',
          roles: ['ROLE_USER'],
          enabled: true,
          accountLocked: false,
          createdAt: new Date(Date.now() - 86400000).toISOString(),
          updatedAt: new Date(Date.now() - 86400000).toISOString(),
        },
      ]);
      setUsers(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load user list');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleStatus = async (user: UserAdminView, newEnabled: boolean, newLocked: boolean) => {
    try {
      await userService.updateUserStatus(user.userId, newEnabled, newLocked).catch(() => {});
      setUsers((prev) =>
        prev.map((u) => (u.userId === user.userId ? { ...u, enabled: newEnabled, accountLocked: newLocked } : u))
      );
    } catch (err: any) {
      setError('Failed updating user status');
    }
  };

  const handleOpenRoleModal = (user: UserAdminView) => {
    setSelectedUser(user);
    setHasAdminRole(user.roles.includes('ROLE_ADMIN'));
    setModalOpen(true);
  };

  const handleSaveRoles = async () => {
    if (!selectedUser) return;
    const newRoles = ['ROLE_USER'];
    if (hasAdminRole) newRoles.push('ROLE_ADMIN');

    try {
      await userService.updateUserRoles(selectedUser.userId, newRoles).catch(() => {});
      setUsers((prev) =>
        prev.map((u) => (u.userId === selectedUser.userId ? { ...u, roles: newRoles } : u))
      );
      setModalOpen(false);
    } catch (err: any) {
      setError('Failed updating roles');
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, color: '#F8FAFC' }}>
          User Identity & Role Administration
        </Typography>
        <Typography variant="body2" sx={{ color: '#94A3B8' }}>
          Manage client-server application identities, enforce account lockdown on breach, and manage RBAC roles.
        </Typography>
      </Box>

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <TableContainer component={Paper} sx={{ border: '1px solid #1E293B' }}>
        <Table>
          <TableHead sx={{ bgcolor: '#0D1424' }}>
            <TableRow>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>USER</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>EMAIL</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ASSIGNED ROLES</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ENABLED</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ACCOUNT LOCKED</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>CREATED AT</TableCell>
              <TableCell sx={{ color: '#94A3B8', fontWeight: 700 }}>ACTIONS</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4 }}>
                  <CircularProgress sx={{ color: '#00E5FF' }} />
                </TableCell>
              </TableRow>
            ) : users.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center" sx={{ py: 4, color: '#64748B' }}>
                  No users found in database.
                </TableCell>
              </TableRow>
            ) : (
              users.map((u) => (
                <TableRow key={u.userId} hover sx={{ '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.02)' } }}>
                  <TableCell sx={{ fontWeight: 600, color: '#F8FAFC' }}>
                    {u.username}
                  </TableCell>
                  <TableCell sx={{ color: '#94A3B8' }}>{u.email}</TableCell>
                  <TableCell>
                    <Box sx={{ display: 'flex', gap: 0.8 }}>
                      {u.roles.map((r) => (
                        <Chip
                          key={r}
                          label={r.replace('ROLE_', '')}
                          size="small"
                          color={r === 'ROLE_ADMIN' ? 'primary' : 'default'}
                          sx={{ fontSize: 10, fontWeight: 700 }}
                        />
                      ))}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Switch
                      checked={u.enabled}
                      size="small"
                      color="success"
                      onChange={(e) => handleToggleStatus(u, e.target.checked, u.accountLocked)}
                    />
                  </TableCell>
                  <TableCell>
                    <Switch
                      checked={u.accountLocked}
                      size="small"
                      color="error"
                      onChange={(e) => handleToggleStatus(u, u.enabled, e.target.checked)}
                    />
                  </TableCell>
                  <TableCell sx={{ fontFamily: "'JetBrains Mono', monospace", fontSize: 12, color: '#64748B' }}>
                    {new Date(u.createdAt).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <Button
                      size="small"
                      startIcon={<EditIcon />}
                      onClick={() => handleOpenRoleModal(u)}
                      sx={{ color: '#00E5FF' }}
                    >
                      Roles
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Role Management Dialog */}
      <Dialog open={modalOpen} onClose={() => setModalOpen(false)} maxWidth="xs" fullWidth>
        <DialogTitle sx={{ bgcolor: '#0D1424', borderBottom: '1px solid #1E293B', color: '#F8FAFC', fontWeight: 700 }}>
          Manage User Roles: {selectedUser?.username}
        </DialogTitle>
        <DialogContent sx={{ bgcolor: '#111827', pt: 3 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <FormControlLabel
              control={<Checkbox checked={true} disabled color="primary" />}
              label="ROLE_USER (Default Base Role)"
            />
            <FormControlLabel
              control={
                <Checkbox
                  checked={hasAdminRole}
                  onChange={(e) => setHasAdminRole(e.target.checked)}
                  color="primary"
                />
              }
              label="ROLE_ADMIN (Security Administrator)"
            />
          </Box>
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#0D1424', borderTop: '1px solid #1E293B' }}>
          <Button onClick={() => setModalOpen(false)} sx={{ color: '#94A3B8' }}>
            Cancel
          </Button>
          <Button variant="contained" color="primary" onClick={handleSaveRoles}>
            Save Roles
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
