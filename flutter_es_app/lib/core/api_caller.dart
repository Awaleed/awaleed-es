import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

class ApiCaller {
  String get baseUrl => _baseUrl;

  static const _baseUrl = 'https://awaleed-es.herokuapp.com';
  static Dio _dio;
  static final PrettyDioLogger _logger = PrettyDioLogger(
    requestHeader: true,
    requestBody: true,
  );

  Dio get dio => _dio;

  Future<T> get<T>({
    @required String path,
    dynamic data,
  }) async {
    _configureDioClient();
    final res = await _dio.get(path, queryParameters: data);
    return res.data;
  }

  Future<T> post<T>({
    @required String path,
    dynamic data,
  }) async {
    _configureDioClient();
    final res = await _dio.post(path, data: data);
    return res.data;
  }

  Future<T> put<T>({
    @required String path,
    dynamic data,
  }) async {
    _configureDioClient();
    final res = await _dio.put(path, data: data);
    return res.data;
  }

  Future<T> delete<T>({
    @required String path,
    dynamic data,
  }) async {
    _configureDioClient();
    final res = await _dio.delete(path, data: data);
    return res.data;
  }

  static List<T> listParser<T>(dynamic data, T Function(dynamic data) parser) {
    final list = <T>[];
    if (data is List) {
      for (final item in data) {
        list.add(parser(item));
      }
    }
    return list;
  }

  static Map<String, dynamic> _getHeaders() {
    return {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };
  }

  static void _configureDioClient() {
    if (_dio != null) return;
    _dio = Dio(
      BaseOptions(
        baseUrl: _baseUrl,
        headers: _getHeaders(),
      ),
    );

    if (kDebugMode) {
      _dio.interceptors.add(_logger);
    }
  }
}
