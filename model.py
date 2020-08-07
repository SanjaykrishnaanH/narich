import math
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, MaxPool2D, Dense, Dropout, Flatten
from tensorflow.keras.callbacks import Callback, ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
import tensorflow.keras.backend as K

class CosineAnnealingScheduler(Callback):
  def __init__(self, T_max, eta_max, eta_min=0, verbose=0):
      super(CosineAnnealingScheduler, self).__init__()
      self.T_max = T_max
      self.eta_max = eta_max
      self.eta_min = eta_min
      self.verbose = verbose

  def on_epoch_begin(self, epoch, logs):
      if not hasattr(self.model.optimizer, 'lr'):
          raise ValueError('Optimizer must have a "lr" attribute\n')
      
      lr = self.eta_min + (self.eta_max - self.eta_min) * (1 + math.cos(math.pi * epoch / self.T_max)) / 2
      
      K.set_value(self.model.optimizer.lr, lr)
      
      if self.verbose > 0:
          print(f'\nEpoch {(epoch+1):5d} CosineAnnealingScheduler - setting learning rate to {lr}')

  def on_epoch_end(self, epoch, logs):
      logs = logs or {}
      logs['lr'] = K.get_value(self.model.optimizer.lr)

def buildModel(input_shape=(128, 128, 3), num_classes=2):
  model = Sequential()
  
  model.add(Conv2D(32, (3, 3), padding='same', input_shape=(128, 128, 3), activation='relu'))
  model.add(Conv2D(64, (3, 3), activation='relu'))
  model.add(MaxPool2D(pool_size=(2, 2)))
  
  model.add(Dropout(0.25))
  
  model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
  model.add(Conv2D(64, (3, 3), activation='relu'))
  model.add(MaxPool2D(pool_size=(2, 2)))
  
  model.add(Dropout(0.5))
  
  model.add(Conv2D(128, (3, 3), padding='same', activation='relu'))
  model.add(Conv2D(128, (3, 3), activation='relu'))
  model.add(MaxPool2D(pool_size=(2, 2)))
  
  model.add(Dropout(0.5))
  
  model.add(Flatten())
  
  model.add(Dense(512, activation='relu'))
  model.add(Dropout(0.5))
  
  if num_classes > 2:
      model.add(Dense(num_classes, activation='softmax'))
      model.compile(RMSprop(lr=0.0005, decay=1e-6), loss="categorical_crossentropy", metrics=["accuracy"])
  
  else:
      model.add(Dense(2, activation='sigmoid'))
      model.compile(RMSprop(lr=0.0005, decay=1e-6), loss="sparse_categorical_crossentropy", metrics=["accuracy"])
  
  model.summary()
  
  return model