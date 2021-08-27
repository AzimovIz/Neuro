from keras.preprocessing.sequence import pad_sequences
import re

#

from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Input


def pre_words(dialog):
    #разделить вопросы/ответы
    que = []
    ans = []
    for i in range(len(dialog)-1):
        que.append(dialog[i])
        ans.append(dialog[i+1])

    # ограничить длинну для вопросов/ответов
    constrain_que = []
    constrain_ans = []
    for i in range(len(que)):
        if len(que[i]) < 20:
            constrain_que.append(que[i])
            constrain_ans.append(ans[i])

    # фильтруем слова с использованием re
    def cleaner(text):
        return text # Она должна быть настроена под каждый язык индивидуальна (Например "прив" заменяем на "привет", "I'm" заменяем на "I am")

    for i in range(len(constrain_que)):
        constrain_que[i] = cleaner(constrain_que[i])
        constrain_ans[i] = cleaner(constrain_ans[i])

    word2count = {}
    for i in range(len(constrain_que)):
        for j in constrain_que[i]:
            if j in word2count:
                word2count[j] += 1
            else:
                word2count[j] = 1
        for j in constrain_ans[i]:
            if j in word2count:
                word2count[j] += 1
            else:
                word2count[j] = 1
    vocab = {
        '<PAD>':0,
        '<EOS>':1,
        '<OUT>':2,
        '<SOS>':3,
    }
    word_num = len(vocab)
    for word, count in word2count.items():
        if count >=3:
            vocab[word] = word_num
            word_num += 1

    return constrain_que, constrain_ans, vocab


def encoder(clean_words, vocab):
    encoder_lst = []
    for line in clean_words:
        lst = []
        for word in line.split():
            if word not in vocab:
                lst.append(vocab['<OUT>'])
            else:
                lst.append(vocab[word])

        encoder_lst.append(lst)

    return encoder_lst

encoder_inp = pad_sequences(encoder(input_mass, slovar), 20, padding='post', truncating='post')
decoder_inp = pad_sequences(encoder(out_mass, slovar), 20, padding='post', truncating='post')

def fin_decoder(decoder_inp):
    dec_fin = []
    for i in decoder_inp:
        dec_fin.append(i[1:])
    return dec_fin

decoder_fin = pad_sequences(fin_decoder(decoder_inp), 20, padding='post', truncating='post')



###############################
#          обучение           #
###############################


enc_inp = Input(shape=(20, ))
dec_inp = Input(shape=(20, ))

voc_size = len(vocab)
embed = Embedding(voc_size+1, output_dim=50,
                  input_length=20,
                  trainable=True)

enc_emb = embed(enc_inp)
enc_lstm = LSTM(400, return_sequences=True, return_state=True)
enc_op, h, c = enc_lstm(enc_emb)
enc_states = [h, c]


dec_emb = embed(dec_inp)
dec_lstm = LSTM(400, return_sequences=True, return_state=True)
dec_op, dh, dc = dec_lstm(dec_emb)

dense = Dense(voc_size, activation='softmax')

dense_op = dense(dec_op)



model = Model([enc_inp, dec_inp], dense_op)


model.compile(loss='categorical_crossentropy',metrics=['acc'],optimizer='adam')

model.fit([encoder_inp, decoder_inp],decoder_final_output,epochs=4)

