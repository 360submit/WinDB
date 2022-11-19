from pydub import AudioSegment
import os

videopath = './Video/'
audiopath = './Audio/'
save_path = './AudioSeg/'

if __name__ == '__main__':
    audio_file = os.listdir(audiopath)
    for hh in range(0, len(audio_file)):

        wav_path = os.path.join(audiopath, audio_file[hh])
        sound = AudioSegment.from_mp3(wav_path)
        duration = int(sound.duration_seconds)*1000

        savepath = os.path.join(save_path, audio_file[hh][:-4])
        if not os.path.exists(savepath): os.makedirs(savepath)

        videopathn = os.path.join(videopath, audio_file[hh][:-4])
        allname = []
        video_file = os.listdir(os.path.join(videopathn))
        for ww in range(len(video_file)):
            if video_file[ww].endswith('.jpg'):
                allname.append(video_file[ww])
        length = len(allname)

        segment = duration/(length//50)
        mm=0
        for ii in range(0, length-1, 50):
            savepaths = os.path.join(savepath,allname[ii][:-4]+'.wav')
            
            
            start_time = mm*segment
            end_time = (mm+1)*segment
            print(start_time)
            print(end_time)
            mm = mm + 1
            word = sound[start_time:end_time]

            word.export(savepaths, format="wav")
