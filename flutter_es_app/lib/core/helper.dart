import 'dart:async';
import 'dart:io';

import 'package:dio/dio.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:supercharged/supercharged.dart';

import 'flash_helper.dart';

abstract class Helpers {
  static void dismissFauces(BuildContext context) {
    FocusScope.of(context).unfocus();
  }

  static Size getWidgetSize(GlobalKey key) {
    final RenderBox renderBox = key.currentContext?.findRenderObject();
    return renderBox?.size;
  }

  static bool isArabic(BuildContext context) => Localizations.localeOf(context).languageCode == 'ar';

  static void showErrorOverlay(
    BuildContext context, {
    @required String error,
  }) {
    final message = error;

    if (context == null) return;

    dismissFauces(context);

    showDialog(
      context: context,
      useRootNavigator: true,
      builder: (context) => AlertDialog(
        title: SelectableText(
          'an error occurred...',
        ),
        content: SelectableText(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('back'),
          ),
        ],
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(25),
        ),
      ),
    );
  }

  static void showErrorDialog(
    BuildContext context, {
    @required dynamic error,
  }) {
    if (context == null) return;

    dismissFauces(context);

    final messageWidget = <Widget>[];

    if (error['errors'] != null && error['errors'] is Map) {
      final map = error['errors'] as Map;
      for (final entrie in map.entries) {
        messageWidget.add(
          SelectableText(
            '${entrie.key}',
            style: Theme.of(context).textTheme.headline6,
          ),
        );
        if (entrie.value is List) {
          for (final str in entrie.value) {
            messageWidget.add(SelectableText('$str'));
          }
        } else {
          messageWidget.add(SelectableText('${entrie.value}'));
        }

        messageWidget.add(const Divider());
      }
    } else if (error['error'] != null) {
      messageWidget.add(SelectableText('${error['error']}'));
    } else {
      messageWidget.add(SelectableText('$error'));
    }
    showDialog(
      context: context,
      useRootNavigator: true,
      builder: (context) => AlertDialog(
        title: SelectableText(
          'an error occurred...',
        ),
        content: Column(
          children: messageWidget,
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: Text('back'),
          ),
        ],
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(25),
        ),
      ),
    );
  }

  static Future<void> showSuccessOverlay(
    BuildContext context, {
    @required String message,
  }) {
    if (context == null) return Future.value();
    final completer = Completer();
    Future.delayed(3.seconds).then((_) => completer.complete());

    FlashHelper.blockSuccessMessage(
      context,
      message: message,
      dismissCompleter: completer,
    );
    return completer.future;
  }

  static Future<void> showMessageOverlay(
    BuildContext context, {
    @required String message,
  }) {
    if (context == null) return Future.value();
    final completer = Completer();
    Future.delayed(3.seconds).then((_) => completer.complete());

    FlashHelper.blockMessage(
      context,
      message: message,
      dismissCompleter: completer,
    );
    return completer.future;
  }

  static DateTime _currentBackPressTime;

  static Future<bool> onWillPop(BuildContext context) {
    final now = DateTime.now();
    if (_currentBackPressTime == null || now.difference(_currentBackPressTime) > const Duration(seconds: 2)) {
      _currentBackPressTime = now;
      Helpers.showMessageOverlay(
        context,
        message: 'tap back again to leave',
      );
      return Future.value(false);
    }
    return Future.value(true);
  }

  static Completer showLoading(BuildContext context) {
    final completer = Completer();
    if (context != null) {
      FlashHelper.blockDialog(context, dismissCompleter: completer);
    }
    return completer;
  }

  static String mapErrorToMessage(dynamic error) {
    try {
      String message;
      if (error is DioError) {
        message = _mapDioError(error);
      } else {
        message = '$error';
      }
      return message;
    } catch (e) {
      return '$error';
    }
  }

  static String _mapDioError(DioError error) {
    final err = error.error;
    if (err is SocketException) {
      if (err?.osError?.errorCode == 7) {
        return 'there is no internet connection';
      }
    }
    if (error.response.data is String) return error.response.data;

    final message = StringBuffer();
    if (error.response?.data['errors'] != null && error.response?.data['errors'] is Map) {
      final map = error.response?.data['errors'] as Map;
      for (final value in map.values) {
        if (value is List) {
          for (final str in value) {
            message.write('$str\n');
          }
        } else {
          message.write('$value\n');
        }
      }
      return message.toString();
    } else if (error.response?.data['error'] != null) {
      return '${error.response?.data['error']}';
    } else {
      return '${error.response?.data}';
    }
  }
}
