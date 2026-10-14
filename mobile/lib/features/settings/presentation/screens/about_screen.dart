import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../theme/app_theme.dart';

/// Screen presenting academic details, framework architecture, and project metadata.
class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('ABOUT FRAMEWORK'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/settings'),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Center(
              child: Icon(Icons.verified_outlined,
                  size: 56, color: AppTheme.accentCyan),
            ),
            const SizedBox(height: 16),
            const Center(
              child: Text(
                'Cloud Native Runtime Protection and API Security Framework',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.white,
                ),
              ),
            ),
            const SizedBox(height: 6),
            const Center(
              child: Text(
                'for Client-Server Mobile Applications',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: AppTheme.accentCyan,
                ),
              ),
            ),
            const SizedBox(height: 24),
            const Card(
              child: Padding(
                padding: EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'PROJECT PURPOSE',
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textMuted,
                      ),
                    ),
                    SizedBox(height: 8),
                    Text(
                      'The central contribution of this project is a reusable, modular '
                      'security framework providing mobile RASP, hardware-backed storage, '
                      'pinned TLS communication, zero-trust API Gateway enforcement, '
                      'asynchronous threat detection, and centralized SIEM observability. '
                      'SecureApp serves as the reference implementation.',
                      style: TextStyle(fontSize: 13, height: 1.4, color: Colors.white70),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 16),
            const Text(
              'FRAMEWORK MODULES',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
                color: AppTheme.textMuted,
              ),
            ),
            const SizedBox(height: 8),
            _buildModuleTile('Module 1', 'Runtime Protection Module (RASP)'),
            _buildModuleTile('Module 2', 'Hardware-Backed Secure Storage'),
            _buildModuleTile('Module 3', 'Secure Pinned Communication'),
            _buildModuleTile('Module 4', 'Authentication & JWT Lifecycle'),
            _buildModuleTile('Module 5', 'Authorization & RBAC'),
            _buildModuleTile('Module 6', 'Spring Cloud Gateway Security'),
            _buildModuleTile('Module 7', 'Request Validation & Sanitization'),
            _buildModuleTile('Module 8', 'Redis Distributed Rate Limiter'),
            _buildModuleTile('Module 9', 'Threat Detection & Anomaly Service'),
            _buildModuleTile('Module 10', 'Security Event & Offline Queue'),
            _buildModuleTile('Module 11', 'Immutable Audit Logging'),
            _buildModuleTile('Module 12', 'Security Analytics & Heuristics'),
            _buildModuleTile('Module 13', 'Prometheus & Grafana Monitoring'),
            _buildModuleTile('Module 14', 'React Admin Operations Dashboard'),
          ],
        ),
      ),
    );
  }

  Widget _buildModuleTile(String badge, String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: AppTheme.cardDark,
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: const Color(0xFF2E4057)),
            ),
            child: Text(
              badge,
              style: const TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: AppTheme.accentCyan,
              ),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              title,
              style: const TextStyle(fontSize: 12, color: Colors.white70),
            ),
          ),
        ],
      ),
    );
  }
}
