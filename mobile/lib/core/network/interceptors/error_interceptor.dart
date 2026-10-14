import 'package:dio/dio.dart';
import '../../constants/security_constants.dart';
import '../../error/exceptions.dart';

/// Interceptor mapping HTTP and network errors into typed security exceptions.
class ErrorInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final String? correlationId = err.requestOptions
        .headers[SecurityConstants.correlationIdHeader] as String?;
    final int? statusCode = err.response?.statusCode;
    final dynamic responseData = err.response?.data;

    String errorMessage = err.message ?? 'Unknown network security failure';
    if (responseData is Map && responseData['message'] != null) {
      errorMessage = responseData['message'].toString();
    }

    if (statusCode == 429) {
      final int retryAfter =
          int.tryParse(err.response?.headers.value('Retry-After') ?? '') ?? 60;
      throw RateLimitExceededException(
        message: errorMessage,
        retryAfterSeconds: retryAfter,
        correlationId: correlationId,
      );
    } else if (statusCode == 401) {
      throw AuthenticationException(errorMessage);
    } else if (statusCode == 403) {
      throw SecurityException(
        errorMessage,
        code: 'FORBIDDEN',
        details: {'correlationId': correlationId, 'status': statusCode},
      );
    } else if (err.type == DioExceptionType.badCertificate) {
      throw const CertificatePinningException();
    }

    handler.next(err);
  }
}
