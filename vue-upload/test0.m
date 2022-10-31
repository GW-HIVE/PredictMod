% trainingData = readtable('fisheriris.csv');
% T2 = readtable("sample1.csv");
% trainClassifier(trainingData);
prediction = Model.predictFcn(T2); %output is a cell value
