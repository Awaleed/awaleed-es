part of 'clause_cubit.dart';

/* 
initial
loading
success
failure
 */

@immutable
abstract class ClauseState {}

class ClauseInitial extends ClauseState {}

class ClauseLoading extends ClauseState {}

class ClauseSuccess extends ClauseState {
  final List<ClauseModel> clause;

  ClauseSuccess(this.clause);
}

class ClauseFailure extends ClauseState {
  final String message;

  ClauseFailure(this.message);
}
