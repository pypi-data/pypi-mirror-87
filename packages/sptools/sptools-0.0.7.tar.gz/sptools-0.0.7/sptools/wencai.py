import requests
import pandas as pd
import random
import logging

def spider_day(date, question, cookie=None, save_path=None, save_name=None):
	url = 'http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data?source=Ths_iwencai_Xuangu&version=2.0&secondary_intent='
	logger = logging.getLogger(str(date))
	logger.setLevel(logging.INFO)
	f = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
	f.setLevel(logging.INFO)
	f.setFormatter(formatter)
	logger.addHandler(f)
	if not cookie:
		cookie = [
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=An5o9WLNrZZQm_myAcrervumz5_Dv0I51IP2HSiH6kG8yxADkE-SSaQTRin7',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=Ap2L2JWInoMf9nqvli-Nu4RbrHKUutEM2-414F9i2fQjFrPuJwrh3Gs-RbXs',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=Aryqu4xHz_DGIfusHxC8iC3MjVFttWDf4ll0o5Y9yKeKYVJNvsUwbzJpRDXl',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AtvNnqcCAN2NnHyp5HVjlfZBajRGsO-y6cSzZs0Yt1rxrPUoVYB_AvmUQ7He',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AvrsYd75ccp09_2mbV4SYp_6Sysfq36F8C_yKQTzpg1Y95SX7DvOlcC_QjHX',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AhkPRPG0ojczIn6j8kPBbzhvKA7wpg1Y95ox7DvOlcC_Qjdyg_YdKIfqQbXI',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AjguJ-hzkyT6nf-ge6TwfMHgCe3JoZwr_gVwr3KphHMmjdbRGrFsu04VQDXB',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AldBCgMuxBGhyECdwImnSWqV5sCinCv-BXCvcqmEcyaN2Hm8sWy7ThVAP8m6',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=AnZg7TrlNX5oI8GaSfJWVjMOx6d7l7rRDNvuNeBfYtn0IxgbSCcK4dxrPkmz',
		'cid=b06575e0076839c8c7d1711418d2ab361600616049; ComputerID=b06575e0076839c8c7d1711418d2ab361600616049; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=a183c8ebf01efdc4e611389bc2fc871a; v=ApWDsC2gZmvXnkKX3tcFI9yDpJpMkkmkE0Yt-Bc6UYxbbrvG3-JZdKOWPcWk'
	]
	params = {
		'question': '{}{}'.format(str(date), str(question)),  # 这里可以进行修改，这里我需要的是消息面消息所有后面写的消息面，如果需要市场关注则将消息面事件改为市场关注即可
		'add_info': {"urp": {"scene": 1, "company": 1, "business": 8}, "contentType": "json"},
		'perpage': 4055,  # 在tushare上查找到目前包括所有股票有4055支
		'page': 1  # 由于一张设置4055支股票所有只用第一个页面即可
	}
	if isinstance(cookie, list):
		for i in range(200):
			try:
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
					, 'Cookie': random.choice(cookie)
				}
				response = requests.post(url=url, headers=headers, data=params)
				result = response.json()
				break
			except:
				continue
	elif isinstance(cookie, str):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
			, 'Cookie': cookie
		}
		response = requests.post(url=url, headers=headers, data=params)
		try:
			result = response.json()
		except Exception:
			logger.info('cookie无效,{}数据爬取失败'.format(date))
			raise ValueError('cookie无效,{}数据爬取失败'.format(date))
	if 'result' in dir():
		logger.info('爬取{}数据成功'.format(date))
		temp = result['data']['answer'][0]['txt'][0]['content']['components'][0]['data'][
			'datas']
	else:
		logger.info('cookie无效,{}数据爬取失败'.format(date))
		raise ValueError('cookie无效,{}数据爬取失败'.format(date))
	df_temp = pd.DataFrame(temp)
	df_temp.dropna(inplace=True)
	df_temp['date'] = str(date)
	df_temp['date'] = df_temp['date'].astype(str)
	df_temp['code'] = df_temp['code'].astype(int)
	for col in df_temp.columns:
		if '[' in col:
			df_temp.rename(columns={col: col.split('[')[0]}, inplace=True)
	if save_path:
		if save_name:
			df_temp.to_csv(save_path + '/{}.csv'.format(str(date)), index=None)
			logger.info('保存{}数据成功'.format(date))
			# print('保存{}数据成功'.format(date))
		else:
			df_temp.to_csv(save_path + '/{}.csv'.format(str(save_name)), index=None)
			logger.info('保存{}数据成功'.format(date))
			# print('保存{}数据成功'.format(date))
	return df_temp