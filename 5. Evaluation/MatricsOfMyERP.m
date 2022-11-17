clear all
close all

GT_fixation = 'C:\CVPR2023\ERPGT\ERPGTTest\Fixation\';
GT_Sal = 'C:\CVPR2023\ERPGTTest\Mask\';
My_Sal = 'C:\CVPR2023\Saliency\result\';
savePath = 'C:\CVPR2023\Saliency\result\';

imgDataDir = dir(My_Sal);
for i = 1:length(imgDataDir)
    if(isequal(imgDataDir(i).name,'.')||... 
    isequal(imgDataDir(i).name,'..')||...
    ~imgDataDir(i).isdir)
        continue;
    end
    imgDir = dir([My_Sal '\' imgDataDir(i).name]); 
    for j =3:length(imgDir)
        if(isequal(imgDir(j).name,'.')||... 
        isequal(imgDir(j).name,'..')||...
        ~imgDir(j).isdir) 
            continue;
        end
        imgDir(j).name
        imgs = dir([My_Sal '\' imgDataDir(i).name '\' imgDir(j).name '\*.png']);
        for k=1:length(imgs)-1
            k
            MySal = im2double(imresize(imread([My_Sal '\' imgDataDir(i).name '\' imgDir(j).name '\' imgs(k).name]),[180,360]));MySal = MySal(:,:,1);
            MySal2 = im2double(imresize(imread([My_Sal2 '\' imgDataDir(i).name '\' imgDir(j).name '\' imgs(k).name]),[180,360]));MySal2 = MySal2(:,:,1);
            MySal = MatrixNormalization(MatrixNormalization(MySal.*MySal2)+MatrixNormalization(MySal+MySal2));
            GTfixation = im2double(imresize(imread([GT_fixation '\' imgDataDir(i).name '\'  imgDir(j).name '\' imgs(k).name(1:end-4) '.png']),[180,360]));GTfixation = GTfixation(:,:,1);
            GTSal = im2double(imresize(imread([GT_Sal '\' imgDataDir(i).name '\' imgDir(j).name '\' imgs(k).name(1:end-4) '.png']),[180,360]));GTSal = GTSal(:,:,1);
            metrics.AUC_Judd(k) = AUC_Judd(MySal, GTfixation);
            metrics.CC(k) = CC(MySal, GTSal);
            metrics.similarity(k) = similarity(MySal, GTSal);
            metrics.NSS(k) = NSS(MySal, GTfixation);
            % metrics.AUC_shuffled1(k) = AUC_shuffled(MySal, eyeMap, shufMap1);
        end
        metrics.CC(isnan(metrics.CC)) = [];
        metrics.CC(metrics.CC==0) = [];
        metrics.similarity(isnan(metrics.similarity)) = [];
        metrics.similarity(metrics.similarity==0) = [];
        metrics.NSS(isnan(metrics.NSS)) = [];
        metrics.NSS(metrics.NSS==0) = [];
        metrics.AUC_Judd(isnan(metrics.AUC_Judd)) = [];
        metrics.AUC_Judd(metrics.AUC_Judd==0) = [];
        % metrics.AUC_shuffled1(isnan(metrics.AUC_shuffled1)) = [];
        %
        metrics_avg_video.CC = mean(metrics.CC);
        metrics_avg_video.similarity = mean(metrics.similarity);
        metrics_avg_video.NSS = mean(metrics.NSS);
        metrics_avg_video.AUC_Judd = mean(metrics.AUC_Judd);
        % metrics_avg_video.AUC_shuffled1 = mean(metrics.AUC_shuffled1);
        
        if exist([savePath '\' imgDataDir(i).name '\'])==0 
            mkdir([savePath '\' imgDataDir(i).name '\']);
        end
        save_path = fullfile([savePath '\' imgDataDir(i).name '\' imgDir(j).name]);
        save(save_path, 'metrics', 'metrics_avg_video');
        clear metrics; clear metrics_avg_video;
    end
end
