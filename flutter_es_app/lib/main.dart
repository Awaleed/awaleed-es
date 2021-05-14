import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'cubits/clause_cubit/clause_cubit.dart';
import 'pages/questions.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) => ClauseCubit(),
      child: MaterialApp(
        theme: ThemeData.dark(),
        home: const QuestionsPage(),
      ),
    );
  }
}
