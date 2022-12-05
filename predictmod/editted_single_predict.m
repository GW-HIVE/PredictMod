function [result] = editted_single_predict()
clear
load('Synth_data_trained_net.mat','Synth_table','net1','net2','net3')%loads k_str, dim_key, Synthetic_data, net1 and net2
%select patient file to upload
%data_mat=table2array(Synth_table(:,2:end));
%% different way to load patient data
%data_table=readmatrix('myData.xls');
%data_table=data_table(:,2:end);
%% in case you want to pick patient

path = 'C:\Users\Julia\PycharmProjects\djangoProject\predictmod\upload\';
File = dir(fullfile(path,'*.xls'));
FileNames = {File.name}'; %change to n lines and 1 column
length = size(FileNames,1);
fullname = strcat(path, FileNames(length));
x = fullname{1,1};
data_table=importdata(x);
%%
input_dat=data_table.data;

[guess]=net123guessfunction(input_dat,net1,net2,net3);
%%
if guess==1
    result = 'Patient is a predicted <strong>responder</strong>';
else
    result = 'Patient is a predicted <strong>non-responder</strong>';
end
%fprintf(result);
%clear data_mat data_table input_dat Synth_table x

%% net guess function
function [guess]=net123guessfunction(input_dat,net1,net2,net3)
all_guess=zeros(1,3);
yguess1=net1(input_dat');all_guess(1)=vec2ind(yguess1);
yguess2=net2(input_dat');all_guess(2)=vec2ind(yguess2);
yguess3=net3(input_dat');all_guess(3)=vec2ind(yguess3);
guess=mode(all_guess);
end
end
