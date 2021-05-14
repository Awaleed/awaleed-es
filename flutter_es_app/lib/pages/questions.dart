import 'package:division/division.dart';
import 'package:flutter/material.dart';
import 'package:flutter_es_app/pages/result.dart';
import 'package:supercharged/supercharged.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_es_app/models/request.dart';

import '../cubits/clause_cubit/clause_cubit.dart';
import '../models/clause.dart';

class QuestionsPage extends StatefulWidget {
  static final route = MaterialPageRoute(builder: (context) => const QuestionsPage());

  const QuestionsPage({Key key}) : super(key: key);

  @override
  _QuestionsPageState createState() => _QuestionsPageState();
}

class _QuestionsPageState extends State<QuestionsPage> {
  PageController pageController;
  RequestModel answers = RequestModel();
  int questionsCount = 0;
  int currentPage = 0;
  bool autoProgress = true;
  @override
  void initState() {
    super.initState();
    pageController = PageController()
      ..addListener(() {
        setState(() {
          currentPage = pageController.page.round();
        });
      });
  }

  @override
  void dispose() {
    pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocConsumer<ClauseCubit, ClauseState>(
        listener: (BuildContext context, ClauseState state) {
          if (state is ClauseInitial) {
            context.read<ClauseCubit>().loadQuestions();
          } else if (state is ClauseSuccess) {
            setState(() {
              questionsCount = state.clause.length;
            });
          }
        },
        builder: (BuildContext context, ClauseState state) {
          if (state is ClauseLoading) {
            return _buildLoading();
          } else if (state is ClauseSuccess) {
            return _buildSuccess(state.clause);
          } else if (state is ClauseFailure) {
            return _buildFailure(state.message);
          } else {
            return Container();
          }
        },
      ),
    );
  }

  Widget _buildLoading() {
    return Center(child: CircularProgressIndicator());
  }

  Widget _buildSuccess(List<ClauseModel> clause) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.end,
          children: [
            IconButton(
              icon: Icon(Icons.settings),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (_) => AlertDialog(
                    content: SizedBox(
                      child: StatefulBuilder(
                        builder: (context, setState) {
                          return Padding(
                            padding: const EdgeInsets.all(10.0),
                            child: Column(
                              // crossAxisAlignment: CrossAxisAlignment.stretch,
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                Text(
                                  'Inference mode',
                                  style: Theme.of(context).textTheme.headline5,
                                ),
                                RadioListTile(
                                  title: Text('forward'),
                                  value: InferenceMode.forward,
                                  groupValue: answers.mode,
                                  onChanged: (value) {
                                    setState(() {
                                      answers.mode = value;
                                    });
                                  },
                                ),
                                RadioListTile(
                                  title: Text('backward'),
                                  value: InferenceMode.backward,
                                  groupValue: answers.mode,
                                  onChanged: (value) {
                                    setState(() {
                                      answers.mode = value;
                                    });
                                  },
                                ),
                                Divider(),
                                CheckboxListTile(
                                  title: Text('Verbose'),
                                  value: answers.verbose,
                                  onChanged: (value) {
                                    setState(() {
                                      answers.verbose = value;
                                    });
                                  },
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                    ),
                  ),
                );
              },
            ),
          ],
        ),
        Expanded(
          child: PageView.builder(
            controller: pageController,
            itemCount: clause.length,
            physics: NeverScrollableScrollPhysics(),
            itemBuilder: (context, index) {
              return QuestionWidget(
                clause: clause[index],
                index: index + 1,
                selectedAnswer: answers.queryParams[index],
                onAnswerSelected: (answer) {
                  setState(() {
                    answers.queryParams[index] = answer;
                  });
                  if (autoProgress) pageController.nextPage(duration: 500.milliseconds, curve: Curves.easeInOut);
                },
              );
            },
          ),
        ),
        LayoutBuilder(builder: (context, constants) {
          double maxWidth;

          if (MediaQuery.of(context).orientation == Orientation.landscape) {
            maxWidth = 1000;
          }

          return SizedBox(
            width: maxWidth,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisSize: MainAxisSize.min,
              children: [
                Padding(
                  padding: const EdgeInsets.only(bottom: 20, left: 20, right: 20),
                  child: Row(
                    children: [
                      if (currentPage != 0)
                        Expanded(
                          child: OutlinedButton(
                            onPressed: () async {
                              await pageController.previousPage(duration: 500.milliseconds, curve: Curves.easeInOut);
                              setState(() {
                                autoProgress = false;
                              });
                            },
                            child: Txt(
                              'Previous',
                              style: TxtStyle()
                                ..fontSize(15)
                                ..padding(all: 10)
                                ..textAlign.center()
                                ..textColor(Colors.blue),
                            ),
                          ),
                        )
                      else
                        Spacer(),
                      Spacer(),
                      if (currentPage != questionsCount - 1)
                        Expanded(
                          child: OutlinedButton(
                            onPressed: () async {
                              await pageController.nextPage(duration: 500.milliseconds, curve: Curves.easeInOut);
                              setState(() {
                                autoProgress = false;
                              });
                            },
                            child: Txt(
                              'Next',
                              style: TxtStyle()
                                ..fontSize(15)
                                ..padding(all: 10)
                                ..textAlign.center()
                                ..textColor(Colors.blue),
                            ),
                          ),
                        )
                      else
                        Spacer()
                    ],
                  ),
                ),
                Txt(
                  'You have answered ${answers.answersCount} of $questionsCount questions',
                  style: TxtStyle()
                    ..fontSize(20)
                    ..padding(all: 10)
                    ..textAlign.center()
                    ..textColor(Colors.white),
                ),
                ElevatedButton(
                  onPressed: answers.answersCount > 0 && answers.validateAnswers ? () => Navigator.of(context).push(ResultPage.route(answers)) : null,
                  child: FittedBox(
                    child: Txt(
                      answers.answersCount > 0 && answers.validateAnswers ? 'Find out' : 'You must answer at least on question',
                      style: TxtStyle()
                        ..fontSize(30)
                        ..maxLines(1)
                        ..padding(all: 20)
                        ..textAlign.center()
                        ..textColor(Colors.white),
                    ),
                  ),
                ),
              ],
            ),
          );
        }),
      ],
    );
  }

  Widget _buildFailure(String message) {
    return Text('Failure: $message');
  }
}

class QuestionWidget extends StatelessWidget {
  const QuestionWidget({
    Key key,
    @required this.clause,
    @required this.selectedAnswer,
    @required this.index,
    @required this.onAnswerSelected,
  }) : super(key: key);

  final ClauseModel clause;
  final String selectedAnswer;
  final ValueChanged<String> onAnswerSelected;
  final int index;
  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constants) {
        final style = ParentStyle()
          ..alignment.center()
          ..elevation(10)
          ..background.color(Colors.grey.shade800)
          ..padding(all: 20)
          ..margin(all: 20);

        if (MediaQuery.of(context).orientation == Orientation.landscape) {
          style..maxWidth(1000);
        }

        return Parent(
          style: style,
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              mainAxisSize: MainAxisSize.min,
              children: [
                Txt(
                  '(Q: $index) ${clause.question}',
                  style: TxtStyle()
                    ..fontSize(30)
                    ..padding(bottom: 20)
                    ..textAlign.center()
                    ..textColor(Colors.white),
                ),
                for (var answer in clause.answers.entries) _buildButton(answer),
                _buildButton(null)
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildButton(MapEntry<String, String> answer) {
    final isSelected = answer?.value == selectedAnswer;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 5),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(primary: Colors.blue.withOpacity(isSelected ? 1 : .5)),
        child: Txt(
          answer?.key ?? "I'm not sure",
          style: TxtStyle()
            ..fontSize(20)
            ..padding(all: 10)
            ..textAlign.center()
            ..textColor(Colors.white),
        ),
        onPressed: () {
          onAnswerSelected(answer?.value);
        },
      ),
    );
  }
}
