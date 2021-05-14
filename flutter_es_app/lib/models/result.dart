import 'dart:convert';

import 'package:flutter/foundation.dart';

class ResultModel {
  ResultModel({
    this.image,
    this.sure,
    this.value,
  });

  final String image;
  final bool sure;
  final List<ValueModel> value;

  ResultModel copyWith({
    String image,
    bool sure,
    List<ValueModel> value,
  }) {
    return ResultModel(
      image: image ?? this.image,
      sure: sure ?? this.sure,
      value: value ?? this.value,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'image': image,
      'sure': sure,
      'value': value?.map((x) => x.toMap())?.toList(),
    };
  }

  factory ResultModel.fromMap(Map<String, dynamic> map) {
    return ResultModel(
      image: map['image'],
      sure: map['sure'],
      value: List<ValueModel>.from(map['value']?.map((x) => ValueModel.fromMap(x))),
    );
  }

  String toJson() => json.encode(toMap());

  factory ResultModel.fromJson(String source) => ResultModel.fromMap(json.decode(source));

  @override
  String toString() => 'ResultModel(image: $image, sure: $sure, value: $value)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is ResultModel && other.image == image && other.sure == sure && listEquals(other.value, value);
  }

  @override
  int get hashCode => image.hashCode ^ sure.hashCode ^ value.hashCode;
}

class ValueModel {
  ValueModel({
    this.percent,
    this.target,
    this.image,
  });

  final double percent;
  final String target;
  final String image;

  ValueModel copyWith({
    double percent,
    String target,
    String image,
  }) {
    return ValueModel(
      percent: percent ?? this.percent,
      target: target ?? this.target,
      image: image ?? this.image,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'percent': percent,
      'target': target,
      'image': image,
    };
  }

  factory ValueModel.fromMap(Map<String, dynamic> map) {
    return ValueModel(
      percent: map['percent'],
      target: map['target'],
      image: map['image'],
    );
  }

  String toJson() => json.encode(toMap());

  factory ValueModel.fromJson(String source) => ValueModel.fromMap(json.decode(source));

  @override
  String toString() => 'ValueModel(percent: $percent, target: $target, image: $image)';

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    return other is ValueModel && other.percent == percent && other.target == target && other.image == image;
  }

  @override
  int get hashCode => percent.hashCode ^ target.hashCode ^ image.hashCode;
}
