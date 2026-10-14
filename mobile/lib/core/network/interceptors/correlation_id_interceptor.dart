import 'package:dio/dio.dart';
import 'package:uuid/uuid.dart';
import '../../constants/security_constants.dart';

/// Interceptor injecting correlation IDs and device fingerprints into every outbound HTTP request.
class CorrelationIdInterceptor extends Interceptor {
  final String deviceId;

  CorrelationIdInterceptor({required this.deviceId});

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    if (!options.headers.containsKey(SecurityConstants.correlationIdHeader)) {
      options.headers[SecurityConstants.correlationIdHeader] =
          const Uuid().v4();
    }

    if (!options.headers.containsKey(SecurityConstants.deviceIdHeader)) {
      options.headers[SecurityConstants.deviceIdHeader] = deviceId;
    }

    handler.next(options);
  }
}
