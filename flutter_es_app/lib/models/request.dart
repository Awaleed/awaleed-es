import 'dart:convert';

import 'package:flutter/foundation.dart';

enum InferenceMode { backward, forward }

class RequestModel {
  Map<int, String> queryParams = {};
  bool verbose = false;
  InferenceMode mode = InferenceMode.backward;

  bool get validateAnswers {
    for (var answer in queryParams.values) {
      if (answer != null) return true;
    }
    return false;
  }

  int get answersCount {
    int count = 0;
    for (var answer in queryParams.values) {
      if (answer != null) count++;
    }
    return count;
  }

  Map<String, dynamic> toMap() {
    StringBuffer queryBuffer = StringBuffer();
    for (var i = 0; i < queryParams.length; i++) {
      if (queryParams[i] == null) continue;
      if (i < queryParams.length - 1) {
        queryBuffer.write(queryParams[i] + ', ');
      } else {
        queryBuffer.write(queryParams[i]);
      }
    }

    return {
      'q': queryBuffer.toString(),
      'v': verbose,
      'm': mode == InferenceMode.backward ? 'backward' : 'forward',
    };
  }

  String toJson() => json.encode(toMap());

  @override
  String toString() => 'RequestModel(queryParams: $queryParams, verbose: $verbose, mode: $mode)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is RequestModel && mapEquals(other.queryParams, queryParams) && other.verbose == verbose && other.mode == mode;
  }

  @override
  int get hashCode => queryParams.hashCode ^ verbose.hashCode ^ mode.hashCode;
}
