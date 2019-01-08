import os
import tflearn
import speech_data as data
import tensorflow as tf

# %matplotlib inline


print("You are using tensorflow version " + tf.__version__)  # tflearn version "+ tflearn.version)
speakers = data.get_speakers()
number_classes = len(speakers)
print("speakers", speakers)

batch = data.wave_batch_generator(batch_size=3000, source=data.Source.DIGIT_WAVES, target=data.Target.speaker)
X, Y = next(batch)

tflearn.init_graph(num_cores=8, gpu_memory_fraction=0.5)
net = tflearn.input_data(shape=[None, 8192])  # Two wave chunks
net = tflearn.fully_connected(net, 64)
net = tflearn.dropout(net, 0.5)
net = tflearn.fully_connected(net, number_classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')

model = tflearn.DNN(net)
model.fit(X, Y, n_epoch=100, show_metric=True, snapshot_step=100)

demo_file = "5_Vicki_260.wav"
demo = data.load_wav_file(data.path + demo_file)
result = model.predict([demo])
result = data.one_hot_to_item(result, speakers)
print("predicted speaker for %s : result = %s " % (demo_file, result))  # ~ 97% correct
