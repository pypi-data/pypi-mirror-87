# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-09-09 15:05:51
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-11-09 17:20:03

import datetime
import time

def getWeek(onlyWeek=False):
	"""
		获取当前是第几周
		返回： float 年份.第几周 如 2020.3
	"""
	week = datetime.datetime.now().isocalendar()
	if not onlyWeek:
		rweek = str(week[0])+'.'+str(week[1]) # 2020.3
	else:
		rweek = week[1]
	return rweek 

def getWeekFirstDayAndLastDay(floatWeek):
	"""
		获取已知第几周的第一天和最后一天

	"""
	tempWeek = str(floatWeek).split('.')
	lastDay = datetime.datetime.strptime(tempWeek[0]+'-'+tempWeek[1]+'-0', '%Y-%U-%w').__format__("%Y-%m-%d") + ' 23:59:59'
	startDay = (datetime.datetime.strptime(tempWeek[0]+'-'+tempWeek[1]+'-0', '%Y-%U-%w')+datetime.timedelta(days=-6)).strftime("%Y-%m-%d %H:%M:%S")
	return startDay,lastDay

def getNowFirstDayAndLastDay():
	"""
		得到当周 第一天和最后一天 ('2020-09-07 00:00:00', '2020-09-13 23:59:59')
	"""
	return getWeekFirstDayAndLastDay(getWeek())


if __name__ == '__main__':
	print(getWeekFirstDayAndLastDay(getWeek()))
	print(getWeek())

