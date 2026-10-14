/// Authenticated user representation.
class UserModel {
  final String id;
  final String username;
  final String email;
  final List<String> roles;
  final bool accountLocked;

  const UserModel({
    required this.id,
    required this.username,
    required this.email,
    required this.roles,
    this.accountLocked = false,
  });

  bool get isAdmin => roles.contains('ROLE_ADMIN');

  factory UserModel.fromMap(Map<String, dynamic> map) {
    return UserModel(
      id: map['id'] as String? ?? '',
      username: map['username'] as String? ?? '',
      email: map['email'] as String? ?? '',
      roles: List<String>.from(map['roles'] as List? ?? ['ROLE_USER']),
      accountLocked: map['accountLocked'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'roles': roles,
      'accountLocked': accountLocked,
    };
  }
}
