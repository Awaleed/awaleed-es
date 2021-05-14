import 'package:bloc/bloc.dart';
import 'package:flutter_es_app/core/api_caller.dart';
import 'package:flutter_es_app/core/helper.dart';
import 'package:meta/meta.dart';

import '../../models/clause.dart';

part 'clause_state.dart';

class ClauseCubit extends Cubit<ClauseState> with ApiCaller {
  ClauseCubit() : super(ClauseInitial()) {
    loadQuestions();
  }

  Future<void> loadQuestions() async {
    emit(ClauseLoading());

    try {
      final res = await get(path: '/clause');
      final clauses = ApiCaller.listParser(res, (data) => ClauseModel.fromMap(data));
      emit(ClauseSuccess(clauses));
    } catch (e) {
      emit(ClauseFailure(Helpers.mapErrorToMessage(e)));
    }
  }
}
