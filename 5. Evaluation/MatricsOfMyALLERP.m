clear all
close all

My_result = 'C:\CVPR2023\Saliency\result\'
savePath = 'C:\CVPR2023\Saliency\result\';
fid1=fopen([savePath, 'final_result.txt'],'w');
for ABI = 1:1
    imgDataDir = dir([My_result, num2str(ABI)]);
    for i = 3:length(imgDataDir)
        vid_res = load(fullfile(My_result, num2str(ABI), imgDataDir(i).name));
        %% Compute Averages per video
        metrics_avg_video.CC(i-2) = vid_res.metrics_avg_video.CC;
        metrics_avg_video.similarity(i-2) = vid_res.metrics_avg_video.similarity;
        metrics_avg_video.NSS(i-2) = vid_res.metrics_avg_video.NSS;
        metrics_avg_video.AUC_Judd(i-2) = vid_res.metrics_avg_video.AUC_Judd;
        % metrics_avg_video.AUC_shuffled1(i) = vid_res.metrics_avg_video.AUC_shuffled1;
    end
    %% Compute All Averages
    metrics_avg_all.CC = mean(metrics_avg_video.CC);
    metrics_avg_all.similarity = mean(metrics_avg_video.similarity);
    metrics_avg_all.NSS = mean(metrics_avg_video.NSS);
    metrics_avg_all.AUC_Judd = mean(metrics_avg_video.AUC_Judd);
    % metrics_avg_all.AUC_shuffled1 = mean(metrics_avg_video.AUC_shuffled1);

    metrics_mat = real(cell2mat( struct2cell( metrics_avg_all ) ) ) 
    
    fprintf(fid1, [num2str(ABI) '\n']);
    fprintf(fid1, 'CC: %0.4f\t', metrics_avg_all.CC);
    fprintf(fid1, 'Similarity: %0.4f\t', metrics_avg_all.similarity);
    fprintf(fid1, 'NSS: %0.4f\t', metrics_avg_all.NSS);
    fprintf(fid1, 'AUC_Judd: %0.4f\n', metrics_avg_all.AUC_Judd);
    %fprintf(fid1, 'AUC_shuffled: %0.4f\n', metrics_avg_all.AUC_shuffled1);
end
fclose(fid1);
