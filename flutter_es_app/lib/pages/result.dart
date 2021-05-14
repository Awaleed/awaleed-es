import 'package:division/division.dart';
import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_es_app/models/request.dart';
import 'package:flutter_es_app/models/result.dart';

import '../cubits/knowledge_cubit/knowledge_cubit.dart';

class ResultPage extends StatelessWidget {
  static route(RequestModel requestModel) => MaterialPageRoute(
        builder: (context) => BlocProvider(
          create: (context) => KnowledgeCubit()..think(requestModel),
          child: const ResultPage(),
        ),
      );

  const ResultPage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: BlocBuilder<KnowledgeCubit, KnowledgeState>(
        builder: (BuildContext context, KnowledgeState state) {
          if (state is KnowledgeLoading) {
            return _buildLoading();
          } else if (state is KnowledgeSuccess) {
            return _buildSuccess(state.result);
          } else if (state is KnowledgeFailure) {
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

  Widget _buildSuccess(ResultModel result) {
    return LayoutBuilder(builder: (context, constants) {
      if (MediaQuery.of(context).orientation == Orientation.landscape) {
        return _buildHorizontal(result);
      } else {
        return _buildVertical(result);
      }
    });
  }

  Widget _buildHorizontal(ResultModel result) {
    return Center(
      child: ConstrainedBox(
        constraints: BoxConstraints(maxWidth: 1000),
        child: Row(
          children: [
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Parent(
                      style: ParentStyle()
                        ..margin(all: 10)
                        ..elevation(5)
                        ..borderRadius(all: 10)
                        ..background.color(Colors.grey.shade800),
                      child: Image.network(
                        result.image,
                        height: 300,
                        fit: BoxFit.contain,
                        loadingBuilder: (context, child, loadingProgress) {
                          double value;
                          if (loadingProgress != null) {
                            value = loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes;
                            return SizedBox(
                              height: 300,
                              child: Center(child: CircularProgressIndicator(value: value)),
                            );
                          } else {
                            return ClipRRect(borderRadius: BorderRadius.circular(10), child: child);
                          }
                        },
                      ),
                    ),
                    _buildSureWidget(result),
                  ],
                ),
              ),
            ),
            Expanded(
              child: SingleChildScrollView(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    for (var result in result.value) ResultWidget(result: result),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  SingleChildScrollView _buildVertical(ResultModel result) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Parent(
            style: ParentStyle()
              ..margin(all: 10)
              ..elevation(5)
              ..borderRadius(all: 10)
              ..background.color(Colors.grey.shade800),
            child: Image.network(
              result.image,
              height: 300,
              fit: BoxFit.contain,
              loadingBuilder: (context, child, loadingProgress) {
                double value;
                if (loadingProgress != null) {
                  value = loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes;
                  return SizedBox(
                    height: 300,
                    child: Center(child: CircularProgressIndicator(value: value)),
                  );
                } else {
                  return child;
                }
              },
            ),
          ),
          _buildSureWidget(result),
          for (var result in result.value) ResultWidget(result: result),
        ],
      ),
    );
  }

  _buildSureWidget(ResultModel result) {
    String value;
    if (result.value.isEmpty) {
      value = 'I don\'t know what this is';
    } else if (result.sure) {
      value = 'I\'have strong feeling on my answer...';
    } else {
      value = 'I\'m not so sure about my answer...';
    }
    return Txt(
      value,
      style: TxtStyle()
        ..fontSize(30)
        ..margin(all: 10)
        ..elevation(5)
        ..background.color(Colors.grey.shade800)
        ..padding(all: 10)
        ..borderRadius(all: 10)
        ..textAlign.center()
        ..textColor(Colors.white),
    );
  }

  Widget _buildFailure(String message) {
    return Text('Failure: $message');
  }
}

class ResultWidget extends StatelessWidget {
  const ResultWidget({Key key, this.result}) : super(key: key);

  final ValueModel result;

  @override
  Widget build(BuildContext context) {
    return Parent(
      style: ParentStyle()
        ..margin(all: 10)
        ..elevation(5)
        ..borderRadius(all: 10)
        ..background.color(Colors.grey.shade800),
      child: Column(
        children: [
          ListTile(
            leading: CircularProgressIndicator(
              value: result.percent / 100,
            ),
            title: Text(result.target),
            subtitle: Text('I\'m sure ${result.percent.toStringAsFixed(2)}%'),
          ),
          Parent(
            style: ParentStyle()
              ..margin(all: 10)
              ..elevation(5)
              ..borderRadius(all: 10)
              ..background.color(Colors.grey.shade800),
            child: Image.network(
              result.image,
              height: 300,
              fit: BoxFit.contain,
              loadingBuilder: (context, child, loadingProgress) {
                double value;
                if (loadingProgress != null) {
                  value = loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes;
                  return SizedBox(
                    height: 300,
                    child: Center(child: CircularProgressIndicator(value: value)),
                  );
                } else {
                  return ClipRRect(
                    borderRadius: BorderRadius.circular(10),
                    child: child,
                  );
                }
              },
            ),
          ),
        ],
      ),
    );
  }
}
