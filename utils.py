import os
import librosa
import numpy as np
import pandas as pd
import librosa.display
import matplotlib.pyplot as plt

dataset_path = 'dataset/texture/'
categories = ['good', 'bad']

def create_spectrogram(filename, class_name, name):
  plt.interactive(False)
  
  clip, sample_rate = librosa.load(filename, sr=None)
  
  fig = plt.figure(figsize=[0.72, 0.72])
  
  ax = fig.add_subplot(111)
  ax.axes.get_xaxis().set_visible(False)
  ax.axes.get_yaxis().set_visible(False)
  ax.set_frame_on(False)
  
  S = librosa.feature.melspectrogram(y=clip, sr=sample_rate)
  
  librosa.display.specshow(librosa.power_to_db(S, ref=np.max))
  
  filename  = 'dataset\\spectrograms\\' + class_name + '\\' + name + '.jpg'
  
  plt.savefig(filename, dpi=400, bbox_inches='tight', pad_inches=0)
  plt.close()    
  fig.clf()
  plt.close(fig)
  plt.close('all')
  
  del filename, name, clip, sample_rate, fig, ax, S

def create_dataset(path = 'dataset/texture', categories = ['good', 'bad']):
  if not os.path.exists("dataset\\spectrograms"):
      os.mkdir("dataset\\spectrograms")
      os.mkdir("dataset\\spectrograms\\good")
      os.mkdir("dataset\\spectrograms\\bad")
      
  for category in categories:
      cat_path = os.path.join(path, category)
      
      for audio in os.listdir(cat_path):
          try:
              create_spectrogram(os.path.join(cat_path, audio), category, audio.split('.')[0])
              
          except Exception as e:
              print(f'Audio at {audio} is corrupted/non-readable/not an audio-file')
              pass