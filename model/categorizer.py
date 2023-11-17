import numpy as np
import re
import os
from keras.utils import pad_sequences
import keras
import pickle




print('loading the ML model ...')
absolute_path = os.path.dirname(__file__)
relative_model_path = "saved-model"
relative_tokenizer_path = "tokenizer"
full_model_path = os.path.join(absolute_path, relative_model_path)
full_tokenizer_path = os.path.join(absolute_path, relative_tokenizer_path)
model = keras.models.load_model(full_model_path)

with open(full_tokenizer_path, 'rb') as fl :
	tokenizer = pickle.load(fl)




def categ(input_text,pk):


	output = {}
	for i , j in zip(input_text,pk):

		text = normalizer(i)
		if text == ' ' or text =='' or text == None:
			text = 'بدون کپشن'
		if len(text) > 750:
			text = text[:749]
		text_list = []
		text_list.append(text)
		inpu = tokenizer.texts_to_sequences(text_list)
		inpu = pad_sequences(inpu, maxlen=750)
		prediction = model.predict(inpu,verbose = 0)
		# confidence is 0.39 and lower than that mean none of classes so its gonna be 4 which mean none
		if np.max(prediction) < 0.39 :
			output[j] = [4]
		else :
			output[j] = list(prediction)[0]




	return output


def remove_emojis(text_input):
	emoj = re.compile("["
					  u"\U0001F600-\U0001F64F"  # emoticons
					  u"\U0001F300-\U0001F5FF"  # symbols & pictographs
					  u"\U0001F680-\U0001F6FF"  # transport & map symbols
					  u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
					  u"\U00002500-\U00002BEF"  # chinese char
					  u"\U00002702-\U000027B0"
					  u"\U00002702-\U000027B0"
					  u"\U000024C2-\U0001F251"
					  u"\U0001f926-\U0001f937"
					  u"\U00010000-\U0010ffff"
					  u"\u2640-\u2642"
					  u"\u2600-\u2B55"
					  u"\u200d"
					  u"\u23cf"
					  u"\u23e9"
				
					  u"\u231a"
					  u"\u200c"
					  u"\ufe0f"  # dingbats
					  u"\u3030"
					  "]+", re.UNICODE)
	return re.sub(emoj, '', text_input)


def normalizer(text_input):
	# normalize the text in a naive way
	text_input = remove_emojis(text_input)
	text_input = re.sub('(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', text_input)
	text_input = re.sub('\d', '', text_input)
	text_input = re.sub("[a-zA-Z&'_,=+]", ' ', text_input)
	text_input = re.sub('[\n]+', ' ', text_input)
	text_input = re.sub('(@[A-Za-z0-9]+)', ' ', text_input)
	text_input = re.sub('#([^ ]+)', ' ', text_input)
	text_input = re.sub('#', ' ', text_input)
	text_input = re.sub('@', ' ', text_input)
	text_input = re.sub('[.)(]|[!]|[”“`⏹]', ' ', text_input)
	text_input = re.sub('[)(•*$&^%~+=<>,]', ' ', text_input)

	text_input = re.sub('؟', ' ', text_input)
	text_input = re.sub('[!]+', ' ', text_input)

	text_input = re.sub('"', '', text_input)
	text_input = re.sub('✔️️', '', text_input)
	text_input = re.sub('⁉', '', text_input)
	text_input = re.sub('،', '', text_input)
	text_input = re.sub('-', ' ', text_input)
	text_input = re.sub('↩', ' ', text_input)
	text_input = re.sub('؛', ' ', text_input)
	text_input = re.sub(':', ' ', text_input)
	text_input = re.sub('»', ' ', text_input)
	text_input = (re.sub('«', ' ', text_input)).strip()
	text_input = re.sub('[ ]+', ' ', text_input)

	return text_input

