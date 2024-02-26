clear
load('Synth_data_trained_net.mat')%loads k_str, dim_key, Synthetic_data, net1 and net2
%select patient file to upload
data_mat=table2array(Synth_table(:,2:end));
%% different way to load patient data
%data_table=readmatrix('myData.xls');
%data_table=data_table(:,2:end);
%% in case you want to pick patient
x = input('Type file name: ','s');
while isfile(x)==0
    fprintf('Could not retrieve file. Verify file is in the correct folder and .xls is included\n')
    x = input('Retype file name: ','s');
end
data_table=importdata(x);
%%
input_dat=data_table.data;
%input_dat=data_table(x,:);
[guess]=net123guessfunction(input_dat,net1,net2,net3);
%%
diary on
if guess==1
    fprintf('Patient is a predicted <strong>responder</strong>\n');
else
    fprintf('Patient is a predicted <strong>non-responder</strong>\n');
end

diary off

%clear data_mat data_table input_dat Synth_table x
%% net guess function
function [guess]=net123guessfunction(input_dat,net1,net2,net3)
all_guess=zeros(1,3);
yguess1=net1(input_dat');all_guess(1)=vec2ind(yguess1);
yguess2=net2(input_dat');all_guess(2)=vec2ind(yguess2);
yguess3=net3(input_dat');all_guess(3)=vec2ind(yguess3);
guess=mode(all_guess);
end