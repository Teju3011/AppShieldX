import { createTheme } from '@mui/material/styles';

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00E5FF', // Cyber Cyan
      contrastText: '#0A0F1D',
    },
    secondary: {
      main: '#818CF8', // Indigo Neon
    },
    error: {
      main: '#F43F5E', // Rose Threat
    },
    warning: {
      main: '#F59E0B', // Amber Alert
    },
    success: {
      main: '#10B981', // Emerald Verified
    },
    background: {
      default: '#0A0F1D',
      paper: '#111827',
    },
    text: {
      primary: '#F8FAFC',
      secondary: '#94A3B8',
    },
    divider: '#1E293B',
  },
  typography: {
    fontFamily: "'Plus Jakarta Sans', -apple-system, sans-serif",
    h1: { fontWeight: 800 },
    h2: { fontWeight: 700 },
    h3: { fontWeight: 700 },
    h4: { fontWeight: 600 },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    button: { textTransform: 'none', fontWeight: 600 },
  },
  shape: {
    borderRadius: 10,
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: '#111827',
          border: '1px solid #1E293B',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 0 15px rgba(0, 229, 255, 0.3)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          fontFamily: "'JetBrains Mono', monospace",
          fontWeight: 600,
        },
      },
    },
  },
});
