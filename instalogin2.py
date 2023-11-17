import numpy as np
from instagrapi import Client
import pickle
from model.categorizer import categ
from collections import Counter
global cl
cl = Client()

# cl.set_proxy()


def login(username , password=None):
	print(username,password)
	if password is None:

		# todo db saving
		with open(f'files/session-{username}') as f:
				session = f.readlines()
		cl.login_by_sessionid(session[0])

	else:
		cl.login(username, password)
		sessions = cl.sessionid
		print(sessions)
		with open(f"files/session-{username}", "w") as text_file:
			text_file.write(sessions)


		# todo db saving








def get_user_likers(list_of_likers):
	output = []
	for i in range(len(list_of_likers)):
		pk = list_of_likers[i].dict()['pk']
		output.append(pk)
	return output


def get_list_of_commentor(list_of_comments):
	output = []
	for i in range(len(list_of_comments)):
		pk = list_of_comments[i].dict()['user']['pk']
		output.append(pk)
	return output


def get_user_media(targetusername,media_number=1):
	cap_list = []
	uid = cl.user_id_from_username(targetusername)
	umedia = cl.user_medias(eval(uid), media_number,sleep=1)
	last_post_pk = umedia[0].dict()['pk']
	caption = umedia[0].dict()['caption_text']
	cap_list.append(caption)
	date = umedia[0].dict()['taken_at']
	last_post_likers_list = cl.media_likers(last_post_pk)
	pk_for_likers = get_user_likers(last_post_likers_list)
	last_post_commentors = cl.media_comments(last_post_pk, 0)
	pk_for_commentors = get_list_of_commentor(last_post_commentors)
	output = list(set(pk_for_commentors + pk_for_likers))
	user_list = [eval(i) for i in output]


	# todo db saving
	# with open(f"files/media-{targetusername}", "wb") as fp:  # Pickling
	# 	pickle.dump(umedia, fp)

	# todo db saving
	with open(f"files/userlist-{targetusername}", "wb") as fpp:  # Pickling
		pickle.dump(user_list, fpp)

	return user_list, cap_list, date,last_post_pk


def get_all_posts_categoris(baseuser):
	uid = cl.user_id_from_username(baseuser)
	umedia = cl.user_medias(eval(uid), 10, sleep=20)
	post_pk = []
	user_captions = []
	for item in umedia:
		post_pk.append(item.dict()['pk'])
		user_captions.append(item.dict()['caption_text'])

	media = categ(user_captions,post_pk)

	new_media = {}
	for i, j in zip(media.values(), media):
		new_media[j] = np.argmax(i)

	number_0 = Counter(new_media.values())[0]  # fardi
	number_1 = Counter(new_media.values())[1]  # zoji va jensi
	number_2 = Counter(new_media.values())[2]  # kodak va nojavan
	number_3 = Counter(new_media.values())[3]  # pish az ezdevaj
	number_4 = Counter(new_media.values())[4]  # uncategorized posts

	info = (f'number of posts >> {len(media)} ''\n number of each categories'
			f'\n fardi {number_0} zoji va jensi {number_1} kodak va nojavan {number_2} pish az ezdevaj {number_3}'
			f' uncategorized posts {number_4}'
			)

	# todo db saving
	with open(f"files/allpostcateg-{baseuser}", "wb") as fppp:  # Pickling
		pickle.dump(new_media, fppp)

	return info


def direct_msg(media_id_to_forward, targetusers:list):
	# media pk to share it and list of target users to direct them
	mtlist = []
	for i in targetusers:
		mtlist.append(i)
		cl.direct_media_share(media_id_to_forward, mtlist)
		mtlist =[]



def get_username_from_id(users_id):
	user_name = []
	for i in users_id:
		user_name.append(cl.username_from_user_id(i))

	return user_name










