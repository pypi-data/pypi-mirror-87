# -*- coding:utf-8 -*-
# @Time: 2020/12/02 01:12
# @Author: jiangwenhao
# @File: wencai.py

import requests
import pandas as pd
import random
import logging
from sptools.cookie_unlock import get_cookies_from_ChromeCore, get_cookies_from_chrome, get_cookies_from_Friefox


def spider_day(date, question, browser, cookie_path=None, cookie=None, save_path=None, save_name=None) -> pd.DataFrame:
	"""
	同花顺问财数据爬取
	Parameters
	----------

	date: int or str 要爬取的日期
	question: str 爬取的问题
	browser: str 现在使用的浏览器名称，不区分大小写
	cookie_path: str 装cookie的路径，可以不填
	save_path: str 爬取数据后保存路径
	save_name: str 爬取数据后保存的名字

	Returns
	-------
	pd.DataFrame
		同花顺问财数据
		Examples:
			----------------------------------
			       code  股票简称      最新价  最新涨跌幅  市场关注度 market_code       股票代码      date
			0    603288  海天味业   165.19  3.763  20764          17  603288.SH  20200910
			1    600519  贵州茅台  1737.00  1.347  16431          17  600519.SH  20200910
			2    600436   片仔癀   220.20  5.349  10167          17  600436.SH  20200910
			3    601318  中国平安    93.38  3.721   8024          17  601318.SH  20200910
			4         2   万科A    30.75  0.163   6872          33  000002.SZ  20200910
			..      ...   ...      ...    ...    ...         ...        ...       ...
			218     823  超声电子    12.64  2.848    311          33  000823.SZ  20200910
			219  601319  中国人保     7.10  2.453    306          17  601319.SH  20200910
			220    2285   世联行     5.30  0.000    305          33  002285.SZ  20200910
			221  300658  延江股份    26.56  1.104    301          33  300658.SZ  20200910
			222  600258  首旅酒店    24.00  3.137    301          17  600258.SH  20200910
			[223 rows x 8 columns]
			----------------------------------
	"""
	logger = logging.getLogger(str(date) + str(browser))
	logger.setLevel(logging.INFO)
	f = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
	f.setLevel(logging.INFO)
	f.setFormatter(formatter)
	logger.addHandler(f)
	if not cookie:
		if browser.lower().title() == 'Chrome':
			if not cookie_path:
				cookie_list = get_cookies_from_chrome()
			else:
				cookie_list = get_cookies_from_chrome(filename=cookie_path)
		elif browser.lower().title() == 'Firefox':
			if not cookie_path:
				cookie_list = get_cookies_from_Friefox()
			else:
				cookie_list = get_cookies_from_Friefox(filename=cookie_path)
		elif browser.lower().title() == 'Chromecore':
			if not cookie_path:
				cookie_list = get_cookies_from_ChromeCore()
			else:
				cookie_list = get_cookies_from_ChromeCore(filename=cookie_path)
		else:
			raise ValueError('当前仅支持Chrome,Firefox,ChromeCore三种浏览器')
		cookie = []
		for coo in cookie_list:
			if '.iwencai.com' in coo.domain:
				cookie.append(coo.value)
		cookie = [
			f'cid=b06575e0076839c8c7d1711418d2ab361600{random.randint(130000, 999999)}; ComputerID=b06575e0076839c8c7d1711418d2ab3616006{random.randint(12000,99999)}; WafStatus=0; other_uid=Ths_iwencai_Xuangu_32967b166d370f213dfd24e0ab7371a9; guideState=1; ver_mark=a; user=MDrFr7flRTo6Tm9uZTo1MDA6NDczNDQwNTUyOjcsMTExMTExMTExMTEsNDA7NDQsMTEsNDA7NiwxLDQwOzUsMSw0MDsxLDEwMSw0MDsyLDEsNDA7MywxLDQwOzUsMSw0MDs4LDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAxLDQwOzEwMiwxLDQwOjI0Ojo6NDYzNDQwNTUyOjE2MDQ0NzMyNDU6OjoxNTM3NzA3NjYwOjI2Nzg0MDA6MDoxYmEzZTM5ZTExMTEzOTM5ZmNlNDg4MTk0ZDc2ODZkMDQ6ZGVmYXVsdF80OjE%3D; userid=463440552; u_name=%C5%AF%B7%E5E; escapename=%25u6696%25u5cf0E; ticket=6c7e349b919a23f142195e1aa1486c2a; user_status=0; PHPSESSID=bd757e7063a03c6f9d996c892bd4ed06; exp_version=1; exp_name=unifiedwap; ' \
			f'v={x}'
			for x in cookie
		]
	if len(cookie) == 0:
		logger.info('传入的cookie为空且本地未储存问财的cookie')
		raise ValueError('传入的cookie为空且本地未储存问财的cookie')
	url = 'http://www.iwencai.com/unifiedwap/unified-wap/v2/result/get-robot-data?source=Ths_iwencai_Xuangu&version=2.0&secondary_intent='
	params = {
		'question': '{}{}'.format(str(date), str(question)),  # 这里可以进行修改，这里我需要的是消息面消息所有后面写的消息面，如果需要市场关注则将消息面事件改为市场关注即可
		'add_info': {"urp": {"scene": 1, "company": 1, "business": 8}, "contentType": "json"},
		'perpage': 4055,  # 在tushare上查找到目前包括所有股票有4055支
		'page': 1  # 由于一张设置4055支股票所有只用第一个页面即可
	}
	if isinstance(cookie, list):
		if browser.lower().title() == 'Firefox':
			for c in cookie:
				try:
					headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
						, 'Cookie': c
					}
					response = requests.post(url=url, headers=headers, data=params)
					result = response.json()
					break
				except:
					continue
		elif browser.lower().title() == 'Chromecore':
			for c in cookie:
				try:
					headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
						, 'Cookie': c
					}
					response = requests.post(url=url, headers=headers, data=params)
					result = response.json()
					break
				except:
					continue
		elif browser.lower().title() == 'Chrome':
			for c in cookie:
				try:
					headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
						, 'Cookie': c
					}
					response = requests.post(url=url, headers=headers, data=params)
					result = response.json()
					break
				except:
					continue

		else:
			raise ValueError('当前仅支持Chrome,Firefox,ChromeCore三种浏览器')
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
	# df_temp.dropna(inplace=True)
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


# 测试区
if __name__ == "__main__":
	data = spider_day(
		date=20200910,
		question='市场关注度',
		browser='ChromeCore',
		# cookie_path=r"C:\Users\jwh\AppData\Local\ChromeCore\User Data\Default\Cookies"
	)
	data = spider_day(
		date=20200910,
		question='市场关注度',
		browser='Firefox',
		# cookie_path=r"C:\Users\jwh\AppData\Roaming\Mozilla\Firefox\Profiles\8ksfov82.default-release\cookies.sqlite"
	)
	data = spider_day(
		date=20200910,
		question='市场关注度',
		browser='Chrome',
		# cookie_path=r"C:\Users\jwh\AppData\Local\Google\Chrome\User Data\Default\Cookies"
	)
	print(data)