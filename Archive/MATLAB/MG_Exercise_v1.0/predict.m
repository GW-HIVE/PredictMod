% Before you run this code, make sure the data table is labeled "data.csv,"
% and your patient with unknown response is labeled "unknown_response.csv".
% You can change these names to the file names saved in your folder. Make
% sure all files needed for this code to run properly are in the same
% folder as this code. 

%Loads Data 
clear
data = readtable('data.csv');
data = data(:, 2:end);

% Split the data into training and test sets
c = cvpartition(data.Status, 'Holdout', 0.25);
train_data = data(c.training, :);
test_data = data(c.test, :);

% Train the classification tree
predictor_vars = data(:, 3:end);
response_var = 'Status';
tree = fitctree(train_data,response_var);

% Make predictions on the test data
unknown_response = readtable('unknown_response.csv');
predictions = predict(tree, unknown_response);
pred = predictions{1};
s = strcat("Your predicted patient response based on metagenomic analysis is ",pred);
disp(s)
