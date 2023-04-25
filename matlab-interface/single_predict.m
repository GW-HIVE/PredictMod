function [result] = single_predict(file_name)

    net1 = [];
    net2 = [];
    net3 = [];

    load /home/pat/gwu-src/predictmod-project/PredictMod/predictmod/Synth_data_trained_net.mat net1 net2 net3;

    data = readmatrix(file_name); 
    data(1) = [];

    %% net guess function
    function [guess]=net123guessfunction(input_dat,net1,net2,net3)
        all_guess=zeros(1,3);
        yguess1=net1(input_dat');all_guess(1)=vec2ind(yguess1);
        yguess2=net2(input_dat');all_guess(2)=vec2ind(yguess2);
        yguess3=net3(input_dat');all_guess(3)=vec2ind(yguess3);
        guess=mode(all_guess);
    end

    [guess]=net123guessfunction(data,net1,net2,net3);
    %%
    if guess==1
        result = 'Patient is a predicted <strong>responder</strong>';
    else
        result = 'Patient is a predicted <strong>non-responder</strong>';
    end
    %fprintf(result);

end
