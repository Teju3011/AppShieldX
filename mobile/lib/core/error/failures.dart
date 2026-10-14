/// Functional failure representation for UI and presentation layers.
abstract class Failure {
  final String message;
  final String? code;

  const Failure(this.message, {this.code});

  @override
  String toString() => '$runtimeType: $message ($code)';
}

class SecurityFailure extends Failure {
  final List<String> detectedThreats;

  const SecurityFailure(
    super.message, {
    super.code = 'SECURITY_FAILURE',
    this.detectedThreats = const [],
  });
}

class NetworkFailure extends Failure {
  final int? statusCode;
  final String? correlationId;

  const NetworkFailure(
    super.message, {
    super.code = 'NETWORK_FAILURE',
    this.statusCode,
    this.correlationId,
  });
}

class AuthFailure extends Failure {
  const AuthFailure(super.message, {super.code = 'AUTH_FAILURE'});
}

class StorageFailure extends Failure {
  const StorageFailure(super.message, {super.code = 'STORAGE_FAILURE'});
}
