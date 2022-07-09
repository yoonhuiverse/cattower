#-*-coding: utf-8-*-
import RPi.GPIO as GPIO
import os
import sys
import random
import time
from gtts import gTTS
from jamo import h2j, j2hcj
from unicode import join_jamos
import pymysql
import speech_recognition as sr


__author__ = 'info-lab'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings (False)

Row = [19,21,23,29,31,33,35,37]
Col = [22, 24, 26, 32, 36, 38, 8]

han1 = ['ㄱ','ㄴ','ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
han2 = ['ㅏ', 'ㅑ', 'ㅓ', 'ㅕ', 'ㅗ', 'ㅛ', 'ㅜ', 'ㅠ', 'ㅡ', 'ㅣ', 'ㅐ', 'ㅒ', 'ㅔ', 'ㅖ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅢ']
han3 = ['ㄲ','ㄸ','ㅃ', 'ㅆ', 'ㅉ', ' ']
eng1=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

Q = '사과 ', '하늘 ', '비행기 ', '우리나라 ', '안녕 ', '만나서 반가워 '
Q1 = 'apple ', 'sky ', 'airplane ', 'korea ', 'hello ', 'box '

text=[]

count = 0
count1 = 0

sound = '한글' #한글 영어

jcnt = 0

conn=None
cur=None
sql=None

langarr =[]
steparr =[]
wordarr =[]
ansarr =[]

n = 0

conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
cur=conn.cursor()


for i in range(8):
        GPIO.setup(Row[i], GPIO.OUT)
for i in range(7):
        GPIO.setup(Col[i], GPIO.IN)

def KeyScan():
	key_scan_line = [0,1,1,1,1,1,1,1]
	key_scan_loop = 0
	getPinData = [0,0,0,0,0,0,0]
	key_num = 0 # 실제 눌린 값

	#키 스캔 반복문
	for key_scan_loop in range(8):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row[0], key_scan_line[0])
		GPIO.output(Row[1], key_scan_line[1])
		GPIO.output(Row[2], key_scan_line[2])
		GPIO.output(Row[3], key_scan_line[3])
		GPIO.output(Row[4], key_scan_line[4])
		GPIO.output(Row[5], key_scan_line[5])
		GPIO.output(Row[6], key_scan_line[6])
		GPIO.output(Row[7], key_scan_line[7])
		time.sleep(0.000001)
		# 키 매트릭스의 열 값 취득
        	# col
		getPinData[0] = not GPIO.input(Col[0])
		getPinData[1] = not GPIO.input(Col[1])
		getPinData[2] = not GPIO.input(Col[2])
		getPinData[3] = not GPIO.input(Col[3])
		getPinData[4] = not GPIO.input(Col[4])
		getPinData[5] = not GPIO.input(Col[5])
		getPinData[6] = not GPIO.input(Col[6])

		if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0 or getPinData[4]!=0 or getPinData[5]!=0 or getPinData[6]!=0):
			if (getPinData[0]==1 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 1
			elif (getPinData[0]==0 and getPinData[1]==1 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 2
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==1 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 3
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==1 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 4
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==1 and getPinData[5]==0 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 5
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==1 and getPinData[6]==0):
				key_num = key_scan_loop*7 + 6
			elif (getPinData[0]==0 and getPinData[1]==0 and getPinData[2]==0 and getPinData[3]==0 and getPinData[4]==0 and getPinData[5]==0 and getPinData[6]==1):
				key_num = key_scan_loop*7 + 7
			print(key_num)
			return key_num

        	#key_scan_line 값을 순차적으로 1비트씩 총 7회 시프트함
		key_scan_line[7] = key_scan_line[6]
		key_scan_line[6] = key_scan_line[5]
		key_scan_line[5] = key_scan_line[4]
		key_scan_line[4] = key_scan_line[3]
		key_scan_line[3] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[0]

		if (key_scan_loop == 7):
			key_scan_line[0] = 0
		else:
			key_scan_line[0] = 1

def KeyScanEng():
	key_scan_line = [0,1,1,1,1,1,1,1]
	key_scan_loop = 0
	getPinData = [0,0,0,0]
	key_num = 0 # 실제 눌린 값

	#키 스캔 반복문
	for key_scan_loop in range(8):
        	# 키 매트릭스의 스캔 라인 설정 출력 값
        	# row
		GPIO.output(Row[0], key_scan_line[0])
		GPIO.output(Row[1], key_scan_line[1])
		GPIO.output(Row[2], key_scan_line[2])
		GPIO.output(Row[3], key_scan_line[3])
		GPIO.output(Row[4], key_scan_line[4])
		GPIO.output(Row[5], key_scan_line[5])
		GPIO.output(Row[6], key_scan_line[6])
		GPIO.output(Row[7], key_scan_line[7])
		time.sleep(0.000001)
		# 키 매트릭스의 열 값 취득
        	# col
		getPinData[0] = not GPIO.input(Col[0])
		getPinData[1] = not GPIO.input(Col[1])
		getPinData[2] = not GPIO.input(Col[2])
		getPinData[3] = not GPIO.input(Col[3])
		#getPinData[4] = not GPIO.input(Col[4])
		#getPinData[5] = not GPIO.input(Col[5])
		#getPinData[6] = not GPIO.input(Col[6])
		#getPinData[7] = not GPIO.input(Col[7])

		if (getPinData[0]!=0 or getPinData[1]!=0 or getPinData[2]!=0 or getPinData[3]!=0):
			key_num = key_scan_loop + getPinData[0] + getPinData[1]*9 + getPinData[2]*17 + getPinData[3]*25
			print(key_num)
			return key_num

        	#key_scan_line 값을 순차적으로 1비트씩 총 7회 시프트함
		key_scan_line[7] = key_scan_line[6]
		key_scan_line[6] = key_scan_line[5]
		key_scan_line[5] = key_scan_line[4]
		key_scan_line[4] = key_scan_line[3]
		key_scan_line[3] = key_scan_line[2]
		key_scan_line[2] = key_scan_line[1]
		key_scan_line[1] = key_scan_line[0]

		if (key_scan_loop == 7):
			key_scan_line[0] = 0
		else:
			key_scan_line[0] = 1

def percent():
	global n
	n=0
	kor1=eng1=0
	conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
	cur=conn.cursor()
	cur.execute('select ans from tblRegister')
	rows = cur.fetchall()
	ansarr.clear()

	for row in rows:
		ansarr.append(row[0])

	for i in ansarr:
		if(n<12 and ansarr[n]=='y'):
			kor1 = kor1+1
		#elif(n>=4 and n<8 and ansarr[n]=='y'):
		#	kor2 = kor2+1
		#elif(n>=8 and n<12 and ansarr[n]=='y'):
		#	kor3 = kor3+1

		elif(n>=12 and ansarr[n]=='y'):
			eng1 = eng1+1
		#elif(n>=16 and n<20 and ansarr[n]=='y'):
		#	eng2 = eng2+1
		#elif(n>=20 and ansarr[n]=='y'):
		#	eng3 = eng3+1
		n=n+1
	return kor1, eng1



def answer(str1):
	conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
	cur=conn.cursor()
	cur.execute("update tblRegister set ans = 'y' where word = '" + str1 +"';")
	conn.commit()




def hangul(num=0):
	global out1
	if(num>=1 and num<15):
                out1 = han1[num-1]
	elif(num>=15 and num<36):
		out1 = han2[num-15]
	elif(num>=36 and num<50):
		out1 = han1[num-36]
	elif(num==50):
		if (out1 == 'ㄱ'):
			out1 = han3[0]
		elif (out1 == 'ㄷ'):
			out1 = han3[1]
		elif (out1 == 'ㅂ'):
			out1 = han3[2]
		elif (out1 == 'ㅅ'):
			out1 = han3[3]
		elif (out1 == 'ㅈ'):
			out1 = han3[4]
		else:
			out1 = '_' # error
	elif(num==51 or num==52 or num==53):
		out1 = han3[5]
	elif(num == 54):
		print("mode1")
	elif(num == 55):
		print("mode2")
	elif(num == 56):
		print("mode3")
	else:
		pass
	print(out1)
	return out1

def voiceinput():
	# microphone에서 auido source를 생성합니다
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Say something!")
		audio = r.listen(source)
	str = r.recognize_google(audio, language='ko-KR')
	# 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
	print("Google Speech Recognition thinks you said : " + str)
	return str

def mode1(a):
	if(count!=23 and count!=6 and count!=41):
		text=a
	elif(count==6 or count==41):
		text=['ㅂ','ㅣ','ㅇ','ㅡ','ㅂ']
	else:
		text=['ㅡ','ㅡ','ㅡ']

	#print(text)
	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count!=51 and count!=52 and text!='_'):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		if ((count >= 36 and count <= 49) or ((out2 == 36 or out2 == 38 or out2 == 41 or out2 == 42 or out2 == 44) and count == 50)):
			#tts = gTTS("받 침", lang='ko', slow=False)
			#tts.save('bat_chim.mp3')
			os.system("omxplayer bat_chim.mp3")

def mode2(a):
	global jcnt, jcnt2
	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
		elif(jcnt2>0):
			jcnt=jcnt2
			jcnt2=0
	elif (count==50):
		if(text[-2]=='ㄴ' or text[-2]=='ㄹ' or text[-2]=='ㅁ' or text[-2]=='ㅇ' or text[-2]=='ㅊ' or text[-2]=='ㅋ' or text[-2]=='ㅌ' or text[-2]=='ㅍ' or text[-2]=='ㅎ'):
			text.insert(-2,text[-2])
		del text[-2]
	if ((count>= 1 and count<=14) or (count>=36 and count<=49)):
		jcnt=jcnt+1
	elif (count>=15 and count<=35):
		if (jcnt==3):
			if(text[-3]=='ㅅ' and text[-4]=='ㄱ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄳ')
			elif(text[-3]=='ㅈ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄵ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄶ')
			elif(text[-3]=='ㄱ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄺ')
			elif(text[-3]=='ㅁ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄻ')
			elif(text[-3]=='ㅂ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄼ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄽ')
			elif(text[-3]=='ㅌ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄾ')
			elif(text[-3]=='ㅍ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄿ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅀ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㅂ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅄ')
		jcnt2 = jcnt
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count == 53):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		text.clear()
		jcnt = 0

def mode3(a):
	global jcnt, A, jcnt2

	text.append(a)
	if(count == 54):
		text.clear()
	elif (count == 52):
		del text[-1]
		del text[-1]
		if(jcnt>0):
			jcnt=jcnt-1
		elif(jcnt2>0):
			jcnt=jcnt2
			jcnt2=0
	elif (count==50):
		if(text[-2]=='ㄴ' or text[-2]=='ㄹ' or text[-2]=='ㅁ' or text[-2]=='ㅇ' or text[-2]=='ㅊ' or text[-2]=='ㅋ' or text[-2]=='ㅌ' or text[-2]=='ㅍ' or text[-2]=='ㅎ'):
			text.insert(-2,text[-2])
		del text[-2]

	if ((count>= 1 and count<=14) or (count>=36 and count<=49)):
		jcnt=jcnt+1
	elif (count>=15 and count<=35):
		if (jcnt==3):
			if(text[-3]=='ㅅ' and text[-4]=='ㄱ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄳ')
			elif(text[-3]=='ㅈ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄵ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄴ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄶ')
			elif(text[-3]=='ㄱ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄺ')
			elif(text[-3]=='ㅁ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄻ')
			elif(text[-3]=='ㅂ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄼ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄽ')
			elif(text[-3]=='ㅌ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄾ')
			elif(text[-3]=='ㅍ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㄿ')
			elif(text[-3]=='ㅎ' and text[-4]=='ㄹ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅀ')
			elif(text[-3]=='ㅅ' and text[-4]=='ㅂ'):
				del text[-3]
				del text[-3]
				text.insert(-2,'ㅄ')
		jcnt2 = jcnt
		jcnt = 0

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count == 53):
		tts = gTTS(merge_jamo, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")
		text.clear()
		jcnt = 0

		print('정답 비교'+A)

		if (A==merge_jamo):
			cur.execute("update tblRegister set ans = 'y' where word = '" + A + "';")
			conn.commit()
			os.system("omxplayer ooo.mp3")
			#os.system("gtts-cli '정답입니다 ' -l ko --output ko_o.mp3")
			#os.system("omxplayer ko_o.mp3")
			kor1, eng1= percent()
			print(kor1) # 0~100:1 step, 100~200:2 step, 200~300:3 step
		else:
			os.system("omxplayer xxx.mp3")
			#os.system("gtts-cli '틀렸습니다. ' -l ko --output ko_x.mp3")
			#os.system("omxplayer ko_x.mp3")

		A = maria_set()
		#A = random.choice(Q)

		print('문제'+A)
		#tts = gTTS('문제', lang='ko', slow=False)
		#tts.save('question.mp3')
		os.system("omxplayer question.mp3")

		tts = gTTS(A, lang='ko', slow=False)
		tts.save('ex_ko.mp3')
		os.system("omxplayer ex_ko.mp3")

def abc(num=0):
	global oute
	if(num>=1 and num<27):
        	oute = eng1[num-1]
	elif(num == 30):
		print("mode1")
	elif(num == 31):
		print("mode2")
	elif(num == 32):
		print("mode3")
	else:
		oute = ' '
	print(oute)
	return oute

def mode4(a): #알파벳 모드1
	text=a
	merge_jamo=join_jamos(text)
	print(merge_jamo)

	if(count1<27):
		tts = gTTS(merge_jamo, lang='en', slow=False)
		tts.save('ex_en.mp3')
		os.system("omxplayer ex_en.mp3")

def mode5(a): #알파벳 모드2
	text.append(a)
	if (count1 == 28):
		del text[-1]
		del text[-1]

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count1 == 29):
		tts = gTTS(merge_jamo, lang='en', slow=False)
		tts.save('ex_en.mp3')
		os.system("omxplayer ex_en.mp3")
		text.clear()

def mode6(a): #알파벳 모드3
	global A
	text.append(a)
	if (count1 == 28):
		del text[-1]
		del text[-1]

	merge_jamo=join_jamos(text)
	print(merge_jamo)
	if(count1 == 29):
		tts = gTTS(merge_jamo, lang='en', slow=False)
		tts.save('ex_en.mp3')
		os.system("omxplayer ex_en.mp3")
		text.clear()

		print('정답 비교'+A)
		if (A==merge_jamo):
			answer(merge_jamo)
			conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
			cur=conn.cursor()
			cur.execute("update tblRegister set ans = 'y' where word = '" + A + "';")
			conn.commit()
			os.system("omxplayer ooo.mp3")
			#os.system("gtts-cli '정답입니다 ' -l ko --output ko_o.mp3")
			#os.system("omxplayer ko_o.mp3")
			kor1, eng1 = percent()
			print(eng1) # 0~100:1 step, 100~200:2 step, 200~300:3 step
		else:
			os.system("omxplayer xxx.mp3")
			#os.system("gtts-cli '틀렸습니다. ' -l ko --output ko_x.mp3")
			#os.system("omxplayer ko_x.mp3")

		A = maria_set()
		#A = random.choice(Q1)
		kor1, eng1 = percent()
		print(eng1) # 0~100:1 step, 100~200:2 step, 200~300:3 step

		print('문제'+A)
		#tts = gTTS('문제', lang='ko', slow=False)
		#tts.save('question.mp3')
		os.system("omxplayer question.mp3")

		tts = gTTS(A, lang='en', slow=False)
		tts.save('ex_en.mp3')
		os.system("omxplayer ex_en.mp3")


def maria_set():
	global n, A #, cur, conn
	n=0
	conn=pymysql.connect(host='localhost', user='root', password='1234', db='mydb', charset='utf8')
	cur=conn.cursor()
	cur.execute('select step, word, ans from tblRegister')
	rows = cur.fetchall()
	ansarr.clear()

	for row in rows:
		steparr.append(row[0])
		wordarr.append(row[1])
		ansarr.append(row[2])

	if(sound == '한글'):
		for i in range(0,12):
			print("i=", i)
			print('st, wo, ans = ', steparr[i], wordarr[i], ansarr[i])

			if(steparr[i]==1 and ansarr[i]=='n'):
				return wordarr[i] # 단어 출력해줌
			else:
				if(steparr[i]==2 and ansarr[i]=='n'):
					return wordarr[i]
				else:
					if(steparr[i]==3 and ansarr[i]=='n'):
						return wordarr[i]

		cur.execute("update tblRegister set ans = 'n';")
		conn.commit()
		return wordarr[0]

	if(sound == '영어'):
		for i in range(12,24):
			print("i=", i)
			print('st, wo, ans = ', steparr[i], wordarr[i], ansarr[i])

			if(steparr[i]==1 and ansarr[i]=='n'):
				return wordarr[i] # 단어 출력해줌
			else:
				if(steparr[i]==2 and ansarr[i]=='n'):
					return wordarr[i]
				else:
					if(steparr[i]==3 and ansarr[i]=='n'):
						return wordarr[i]

		cur.execute("update tblRegister set ans = 'n';")
		conn.commit()
		return wordarr[12]


# main
while True:
	try:
		if(sound == '한글'):
			#tts=gTTS("현재 모드 한 그을", lang='ko', slow=False)
			#tts.save('mode_kor.mp3')
			os.system("omxplayer mode_kor.mp3")
			os.system("omxplayer mode_sel.mp3")

			count = 0
			count1 = 0
			#tts=gTTS("모드를 선택해주세요.", lang='ko', slow=False)
			#tts.save('mode_sel.mp3')
			#os.system("omxplayer mode_sel.mp3")

			while True:
				if(count==54):
					#tts = gTTS("모드 일번 입니다. 자음, 모음을 입력해주세요.", lang='ko', slow=False)
					#tts.save('mode_1.mp3')
					os.system("omxplayer mode_1.mp3")
					while True:
						out2 = count
						count = KeyScan() #count = int(input())
						time.sleep(0.5)
						if(count == 54 or count == 55 or count == 56):
							break
						elif((count == 53 and (not join_jamos(text).strip()))):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count)) == "<class 'int'>"):
							mode1(hangul(count))
						else:
							print("error")
				elif(count==55):
					#tts = gTTS("모드 이번 입니다. 단어 또는 문장을 입력해주세요. ", lang='ko', slow=False)
					#tts.save('mode_2.mp3')
					os.system("omxplayer mode_2.mp3")
					while True:
						count = KeyScan() #count = int(input())
						time.sleep(0.5)
						if(count == 54 or count == 55 or count == 56):
							text.clear()
							break
						elif((count == 53 and (not join_jamos(text).strip()))):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count)) == "<class 'int'>"):
							mode2(hangul(count))

						else:
							print("error")
				elif(count==56): # mode3
					#tts = gTTS("모드 삼번 입니다. 문제", lang='ko', slow=False)
					#tts.save('mode_3.mp3')
					os.system("omxplayer mode_3.mp3")

					A = maria_set()
					#A = random.choice(Q)

					print('_'+A+'_')

					tts = gTTS(A, lang='ko', slow=False)
					tts.save('ex_ko.mp3')
					os.system("omxplayer ex_ko.mp3")

					while True:
						count = KeyScan() #count = int(input())
						time.sleep(0.5)
						if(count==54 or count==55 or count==56):
							text.clear()
							break
						elif(count == 53 and (not join_jamos(text).strip())):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count)) == "<class 'int'>"):
							mode3(hangul(count))
						else:
							print("error")
				else:
					count = KeyScan() #count = int(input())
					print(count)
					if(count == 53):
						sound = '1'
						break
					time.sleep(0.5)
		elif(sound == '영어'): #카운트 바꾸기
			#tts=gTTS("현재 모드 영 어 ", lang='ko', slow=False)
			#tts.save('mode_eng.mp3')
			os.system("omxplayer mode_eng.mp3")
			count = 0
			count1 = 0
			# tts=gTTS("모드를 선택해주세요.", lang='ko', slow=False)
			# tts.save('mode_sel.mp3')
			os.system("omxplayer mode_sel.mp3")

			while True:
				if (count1 == 30):
					#tts = gTTS("모드 일번 입니다. 알파벳을 입력해주세요.", lang='ko', slow=False)
					#tts.save('mode_4.mp3')
					os.system("omxplayer mode_4.mp3")
					while True:
						out2 = count1
						count1 = KeyScanEng() # count1 = int(input())
						time.sleep(0.5)
						if (count1 == 30 or count1 == 31 or count1 == 32):
							break
						elif((count1 == 29 and (not join_jamos(text).strip()))):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count1)) == "<class 'int'>"):
							mode4(abc(count1))
						else:
							print("error")
				elif (count1 == 31):
					#tts = gTTS("모드 이번 입니다. 단어 또는 문장을 입력해주세요. ", lang='ko', slow=False)
					#tts.save('mode_5.mp3')
					os.system("omxplayer mode_5.mp3")
					while True:
						count1 = KeyScanEng() # count = int(input())
						time.sleep(0.5)
						if (count1 == 30 or count1 == 31 or count1 == 32):
							text.clear()
							break
						elif((count1 == 29 and (not join_jamos(text).strip()))):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count1)) == "<class 'int'>"):
							mode5(abc(count1))

						else:
							print("error")
				elif (count1 == 32):  # mode3
					#tts = gTTS("모드 삼번 입니다. 문제", lang='ko', slow=False)
					#tts.save('mode_6.mp3')
					os.system("omxplayer mode_6.mp3")

					A = maria_set()
					#A = random.choice(Q1)

					print('_' + A + '_')

					tts = gTTS(A, lang='en', slow=False)
					tts.save('ex_en.mp3')
					os.system("omxplayer ex_en.mp3")

					while True:
						count1 = KeyScanEng() # count1 = int(input())
						time.sleep(0.5)
						if (count1 == 30 or count1 == 31 or count1 == 32):
							text.clear()
							break
						elif((count1 == 29 and (not join_jamos(text).strip()))):
							os.system("omxplayer mode_sel.mp3")
							break
						elif (str(type(count1)) == "<class 'int'>"):
							mode6(abc(count1))
						else:
							print("error")
				else:
					count1 = KeyScanEng() # count1 = int(input())
					print(count1)
					if(count1 == 29):
						sound = '2'
						break
					time.sleep(0.5)

		else:
			# 언어 선택
			#tts = gTTS("언어를 선택하세요. 한글, 영어", lang='ko', slow=False)
			#tts.save('lan.mp3')
			os.system("omxplayer lan.mp3")
			print('언어 선택')

			sound = voiceinput()
			print(sound)
			'''
			if(sound == voiceinput()):
				sound = '영어'
			else:
				sound = '한글'
			'''
			'''
			if(count==53):
				sound = '영어'
			'''

	except KeyboardInterrupt:
		# Ctrl + C
		GPIO.cleanup()
		sys.exit()
	except sr.UnknownValueError:
		print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
		print("Could not request results from Google Speech Recognition service; {0}".format(e))
	except:
		#print('error')
		print("문제가 많다")
		#tts = gTTS("아무것도 입력되지 않았습니다.  모드를 다시 선택해주세요", lang='ko', slow=False)
		#tts.save('mode_error.mp3')
		#os.system("omxplayer mode_error.mp3")
		pass