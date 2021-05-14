import 'package:bloc/bloc.dart';
import 'package:meta/meta.dart';

import '../../core/api_caller.dart';
import '../../core/helper.dart';
import '../../models/request.dart';
import '../../models/result.dart';

part 'knowledge_state.dart';

class KnowledgeCubit extends Cubit<KnowledgeState> with ApiCaller {
  KnowledgeCubit() : super(KnowledgeInitial());

  Future<void> think(RequestModel requestModel) async {
    emit(KnowledgeLoading());

    try {
      final res = await post(path: '/think', data: requestModel.toMap());
      final result = ResultModel.fromMap(res);
      emit(KnowledgeSuccess(result));
    } catch (e) {
      emit(KnowledgeFailure(Helpers.mapErrorToMessage(e)));
    }
  }
}
