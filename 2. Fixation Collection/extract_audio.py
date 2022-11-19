import os

videopath = './Videos/'
savepath = './Audio/'
import moviepy.editor as mp
def extract_audio(videos_file_path,save_path):
    my_clip = mp.VideoFileClip(videos_file_path)
    my_clip.audio.write_audiofile(f'{save_path}.wav')

def Vid2Frm():
    seqs = os.listdir(os.path.join(videopath))
    for seq in seqs:
        seq_path = os.path.join(videopath, seq)
        save_path = os.path.join(savepath, seq[:-4])
        extract_audio(seq_path,save_path)


if __name__ == '__main__':
    Vid2Frm()