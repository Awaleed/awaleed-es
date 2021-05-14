part of 'knowledge_cubit.dart';

@immutable
abstract class KnowledgeState {}

class KnowledgeInitial extends KnowledgeState {}

class KnowledgeLoading extends KnowledgeState {}

class KnowledgeSuccess extends KnowledgeState {
  final ResultModel result;

  KnowledgeSuccess(this.result);
}

class KnowledgeFailure extends KnowledgeState {
  final String message;

  KnowledgeFailure(this.message);
}
