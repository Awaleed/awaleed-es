import 'dart:convert';

import 'package:flutter/foundation.dart';

class ClauseModel {
  ClauseModel({
    this.question,
    this.answers,
  });

  final String question;
  final Map<String, String> answers;

  ClauseModel copyWith({
    String question,
    Map<String, String> answers,
  }) {
    return ClauseModel(
      question: question ?? this.question,
      answers: answers ?? this.answers,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'question': question,
      'answers': answers,
    };
  }

  factory ClauseModel.fromMap(Map<String, dynamic> map) {
    return ClauseModel(
      question: map['question'],
      answers: Map<String, String>.from(map['answers']),
    );
  }

  String toJson() => json.encode(toMap());

  factory ClauseModel.fromJson(String source) => ClauseModel.fromMap(json.decode(source));

  @override
  String toString() => 'ClauseModel(question: $question, answers: $answers)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is ClauseModel && other.question == question && mapEquals(other.answers, answers);
  }

  @override
  int get hashCode => question.hashCode ^ answers.hashCode;
}
