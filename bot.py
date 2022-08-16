from requests import get
from re import findall
import os
import glob
from rubika.client import Bot
import requests
from rubika.tools import Tools
from rubika.encryption import encryption
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import random
import urllib
import io
import asyncio

bot = Bot("AppName", auth="rzpqkiypkrtnshneyaqerixnaptwamoe", displayWelcome=False)
target = "g0BsCEp0a05f7d33169874830aeb4e90"

creator = open('botAdmins.txt','r').read().split('\n')

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me","gif","GIF","Gif"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گزاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/5) اخطار دریافت کرده اید .\n\nپس از دریافت 5 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/5) اخطار دریافت کرده اید .\n\nپس از دریافت 5 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (3/5) اخطار دریافت کرده اید .\n\nپس از دریافت 5 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
		
	elif coun == 4:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (4/5) اخطار دریافت کرده اید .\n\nپس از دریافت 5 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
		
	elif coun == 5:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (5/5) اخطار دریافت کرده اید .\n\nپس از دریافت 5 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
		bot.banGroupMember(target, guid)


while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

								
						elif msg.get("text").startswith("ایجاد کال"):
							try:
								bot.startVoiceChat(target)
								bot.sendMessage(target, "✅ با موفقیت ایجاد شد", message_id=msg.get("message_id"))
							except:
								print("err call")
							

						elif msg.get("text") == "خاموش" or msg.get("text") == "/stop" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "✅ ربات اکنون خاموش است", message_id=msg.get("message_id"))
							except:
								print("err off bot")
								
						elif msg.get("text") == "راه اندازی مجدد" or msg.get("text") == "/restart" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "در حال راه اندازی مجدد...", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت مجددا راه اندازی شد!", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
								
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را درست وارد کنید!", message_id=msg.get("message_id"))
								

						elif msg.get("text").startswith("ریم") and msg.get("author_object_guid") in admins :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ با موفقیت از گروه ریم شد.", message_id=msg.get("message_id"))
								else :
									bot.sendMessage(target, "❌ کاربر ادمین نیست!", message_id=msg.get("message_id"))
									
							except IndexError:
								bot.banGroupMember(target, bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"])
								# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ دستور اشتباه است! ", message_id=msg.get("message_id"))

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدوددی! ", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را درست وارد کنید. ", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه است!", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "دستورات":
							try:
								rules = open("dastorat.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت دستورات") and msg.get("author_object_guid") in admins:
							try:
								rules = open("gavanin.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "دستو‌رات ربا‌ت به‌روزرسانی شد.", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "مشکلی پیش آمد دوباره تلاش کنید.", message_id=msg.get("message_id"))
							
						elif msg.get("text").startswith("زمان"):
							try:
								response = get("https://api.codebazan.ir/time-date/?td=all").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
								
						elif msg.get("text").startswith("اسم شاخ"):
							try:
								responser = get(f"https://api.codebazan.ir/name/").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("جوک فامیلی"):
							try:
								responser = get(f"https://api.chabk.ir/api/jok/family").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("اعتراف"):
							try:
								responser = get(f"https://api.chabk.ir/api/jok/confess").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("مورد داشتیم"):
							try:
								responser = get(f"https://api.chabk.ir/api/jok/we-had-case").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("دقت کردین"):
							try:
								responser = get(f"https://api.chabk.ir/api/jok/precision").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("خاطره") or msg.get("text").startswith("khatere") or msg.get("text").startswith("!khatere"):
							try:
								response = get("https://api.codebazan.ir/jok/khatere/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("طلا"):
							try:
								response = get("https://api.codebazan.ir/arz/?type=tala").json()
								sekeamam = response[0]["price"]
								nimseke = response[1]["price"]
								robseke = response[2]["price"]
								sekegeramy = response[3]["price"]
								onstala = response[4]["price"]
								onsnoghre = response[5]["price"]
								sekebaharazadi = response[6]["price"]
								bot.sendMessage(target, f"قیمت سکه امام : {sekeamam} \n قیمت نیم سکه : {nimseke} \n قیمت ربع سکه : {robseke} \n قیمت گرمی سکه : {sekegeramy} \n قیمت انس طلا : {onstala} \n قیمت انس نقره : {onsnoghre} \n قیمت سکه بهار ازادی : {sekebaharazadi}",message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("خوش آمدم") or msg.get("text").startswith("خوش اومدم"):
							try:
								bot.sendMessage(target, "خب به من چه!", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("منی") or msg.get("text").startswith("معنی") or msg.get("text").startswith("!mani"):
							try:
								response = get("https://api.codebazan.ir/vajehyab/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
								
						elif msg.get("text").startswith("هوی") or msg.get("text").startswith("حوی‌"):
							try:
								bot.sendMessage(target, "چیه مگه؟😂😆", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("بای"):
							try:
								bot.sendMessage(target, "دوست عزیز لطفا از کلمه *بای* استفاده نکیند❗ 	بای ریشه فرانسوی دارد و به معنای دوستی با شیطان ميباشد🥀 به جای استفاده از این کلمات بیایید از کلمات فارسی و بومی خودمون استفاده کنیم مثلا خدانگهدار👋", message_id=msg.get("message_id"))
							except:
								print("err bay")
								
						elif msg.get("text").startswith("چخبر") or msg.get("text").startswith("چه خبر"):
							try:
								bot.sendMessage(target, "سلامتیت عزیز دلم تو چخبر", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
										
						elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "خوبم تو خوبی؟🤪", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("بوس") or msg.get("text").startswith("بوص"):
							try:
								bot.sendMessage(target, "💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋💋", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("خدافظ") or msg.get("text").startswith("خدا حافظ"):
							try:
								bot.sendMessage(target, "خدا نگه دار👋", message_id=msg.get("message_id"))
							except:
								print("err answer hay")			  
								
										
					    			
								
								
						elif msg.get("text").startswith("اصکی") or msg.get("text").startswith("اسکی"):
							try:
								bot.sendMessage(target, "نرو لیز میخوری😂", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
								
								
						elif msg.get("text").startswith("دوست دارم") or msg.get("text").startswith("دوصت دارم"):
							try:
								bot.sendMessage(target, "عشقم منم دوست دارم😍", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("عاجگتم") or msg.get("text").startswith("عاشقتم"):
							try:
								bot.sendMessage(target, "منم عاشقتم نفص🤪🤤", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
								
						
								
								
						
								
								
						elif msg.get("text").startswith("میگم با من ازدواج میکنی") or msg.get("text").startswith("با من ازدواج میکنی"):
							try:
								bot.sendMessage(target, "بلهههه🤗❤", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
					  							
								
						elif msg.get("text").startswith("جر") or msg.get("text").startswith("من جر"):
							try:
								bot.sendMessage(target, "نخور سوزن ندارم بدوزمت🥴", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("ناموسا") or msg.get("text").startswith("ناموصا"):
							try:
								bot.sendMessage(target, "عمت اومد پا بوسم", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
								
								
						elif msg.get("text").startswith("قربونت") or msg.get("text").startswith("گربونت"):
							try:
								bot.sendMessage(target, "فرغونت سرش بگیر ب دندونت", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("افرین") or msg.get("text").startswith("آفرین") or msg.get("text").startswith("آفلین") or msg.get("text").startswith("افلین"):
							try:
								bot.sendMessage(target, "ممنون جناب🤪", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
								
						elif msg.get("text").startswith("رل میخوام") or msg.get("text").startswith("رل میقام"):
							try:
								bot.sendMessage(target, "منم عمتو میخوام🤗", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("چعجب") or msg.get("text").startswith("چه عجب"):
							try:
								bot.sendMessage(target, "دست بهش زدی شد سه وجب", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("بغل") or msg.get("text").startswith("بقل"):
							try:
								bot.sendMessage(target, "اخی بدو بیا بغلم🥺🤗", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("ای جان") or msg.get("text").startswith("ع جان"):
							try:
								bot.sendMessage(target, "جووون بخورمت", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("💔") or msg.get("text").startswith("💔💔"):
							try:
								bot.sendMessage(target, "نشکونش🥺🥀", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("به عنم") or msg.get("text").startswith("ب عنم"):
							try:
								bot.sendMessage(target, "به کیررررررمممم", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						
								
								
						elif msg.get("text").startswith("🚶‍♂️") or msg.get("text").startswith("🚶‍♀️‍️") in admins :
							try:
								bot.sendMessage(target, "بیا بشین ببینم چته", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
						
											
								
								
						elif msg.get("text").startswith(".") or msg.get("text").startswith("..") in admins :
							try:
								bot.sendMessage(target, "اخی دلم برا اونایی که نقطه میدن میسوزه", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
						elif msg.get("text").startswith("هعی") or msg.get("text").startswith("هیب") in admins :
							try:
								bot.sendMessage(target, "چیشده جیگر🥺", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
						elif msg.get("text").startswith("عمم") or msg.get("text").startswith("ن پس عمم") in admins :
							try:
								bot.sendMessage(target, "نگیرررر اسمشو اووووف عمت بیارم ببرمش بازار🥲😂🔥", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
						
												
									
						
								
								
						elif msg.get("text").startswith("نپس") or msg.get("text").startswith("نفس"):
							try:
								bot.sendMessage(target, "جان نفس🤤", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
						elif msg.get("text").startswith("ب کوصم") or msg.get("text").startswith("بکوصم"):
							try:
								bot.sendMessage(target, "ای جاان کوصتو بخورم؟🤤", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
						
								
								
								
								
						elif msg.get("text").startswith("رل پی") or msg.get("text").startswith("رل پیوی"):
							try:
								bot.sendMessage(target, "رلم میشی؟", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
								
						elif msg.get("text").startswith("عجب") or msg.get("text").startswith("عژب"):
							try:
								bot.sendMessage(target, "مش رجب🌚", message_id=msg.get("message_id"))
							except:
								print("err answer fosh")
								
								
								
								
								
						
										
						elif msg.get("text").startswith("چطوری") or msg.get("text").startswith("شطوری"):
							try:
								bot.sendMessage(target, "عالیم جیگر😍", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("خوبم") or msg.get("text").startswith("خبم"):
							try:
								bot.sendMessage(target, "شکر", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						
								
						elif msg.get("text").startswith("شب بخیر") or msg.get("text").startswith("شب خوش"):
							try:
								bot.sendMessage(target, "خوب بخوابی عزیزم", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("صب بخیر") or msg.get("text").startswith("صبح بخیر"):
							try:
								bot.sendMessage(target, "صبح تو هم بخیر", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("صبخیر") or msg.get("text").startswith("صوبخیر"):
							try:
								bot.sendMessage(target, "عشقم خوب خوابیدی😍", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
					    
								
								
						elif msg.get("text").startswith("شو خوش") or msg.get("text").startswith("شبخیر"):
							try:
								bot.sendMessage(target, "شبت شیک", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						elif msg.get("text").startswith("خوابم میاد") or msg.get("text").startswith("میرم بخوابم"):
							try:
								bot.sendMessage(target, "گمشو بخواب تنبل😂", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
								
						
								
								
						elif msg.get("text").startswith("حوصلم") or msg.get("text").startswith("حصلم"):
							try:
								bot.sendMessage(target, "شلوارت در بیار بکش سرت😆", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						
																							
																							
								
						elif msg.get("text").startswith("چه خبر") or msg.get("text").startswith("چخبر"):
							try:
								bot.sendMessage(target, "ســلامـتیت😍♥", message_id=msg.get("message_id"))
							except:
								print("err CheKhabar")
								
						elif msg.get("text").startswith("ربات") or msg.get("text").startswith("بات"):
							try:
								bot.sendMessage(target, "جونم عشقم🥲❤", message_id=msg.get("message_id"))
							except:
								print("err bot answer")
								
						
								
								
						
								
								
						elif msg.get("text").startswith("اومدم") or msg.get("text").startswith("امدم"):
							try:
								bot.sendMessage(target, "‌‌‌‌‌‌‌‌‌‌‌‌‌‌‌ب کتفم خا", message_id=msg.get("message_id"))
							except:
								print("err answer answer")
								
						elif msg.get("text") == "ساعت":
							try:
								bot.sendMessage(target, f"Time : {time.localtime().tm_hour} : {time.localtime().tm_min} : {time.localtime().tm_sec}", message_id=msg.get("message_id"))
							except:
								print("err time answer")
						
						elif msg.get("text") == "تاریخ":
							try:
								bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))
							except:
								print("err date")
								
						elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "پیام حذف شد.", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("حساب") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "دستور اشتباه است! " ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
								
						elif msg.get("text").startswith("سلام") or msg.get("text").startswith("سلم") or msg.get("text").startswith("صلام") or msg.get("text").startswith("صلم") or msg.get("text").startswith("سیلام") or msg.get("text").startswith("صیلام"): 
							try:
								bot.sendMessage(target, 'ســلـــــــــــام🥰😘' ,message_id=msg.get("message_id"))
							except:
								print("err hello")
								
						elif msg.get("text").startswith("😂") or msg.get("text").startswith("🤣"):
							try:
								bot.sendMessage(target, "نخند میترکی.", message_id=msg.get("message_id"))
							except:
								print("err luagh")
								
						elif msg.get("text") == "لینک":
							try:
								rules = open("link.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")	
								
						elif msg.get("text") == "😐":
							try:
								bot.sendMessage(target, "😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.pin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر با موفقیت سنجاق شد!", message_id=msg.get("message_id"))
							except:
								print("err pin")
								
						elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.unpin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر از سنجاق برداشته شد!", message_id=msg.get("message_id"))
							except:
								print("err unpin")
								
						elif msg.get("text").startswith("ترجمه"):
							try:
								responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
								al = [responser["result"]]
								bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم??", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("فونت"):
							try:
								response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
								bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						
						
						elif msg.get("text").startswith("جوک") or msg.get("text").startswith("jok") or msg.get("text").startswith("!jok"):
							try:
								response = get("https://api.codebazan.ir/jok/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
						
								
						elif msg.get("text").startswith("ارسال") :
						        bot.sendMessage(bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"], "یک پیام ناشناس دارید جناب⬅️\n"+" ".join(msg.get("text").split(" ")[2:]))
						        bot.sendMessage(target,f"یک پیام ناشناس ارسال شد✅", message_id=msg.get("message_id"))
								
						elif msg["text"].startswith("!number") or msg["text"].startswith("بشمار"):
							try:
								response = get(f"http://api.codebazan.ir/adad/?text={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
								
						
							
						elif msg.get("text").startswith("تاریخ میلادی"):
							try:
								response = get("Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
							
						elif msg.get("text").startswith("ذکر") or msg.get("text").startswith("zekr") or msg.get("text").startswith("!zekr"):
							try:
								response = get("http://api.codebazan.ir/zekr/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("حدیث") or msg.get("text").startswith("hadis") or msg.get("text").startswith("!hadis"):
							try:
								response = get("http://api.codebazan.ir/hadis/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("بیو") or msg.get("text").startswith("bio") or msg.get("text").startswith("!bio"):
							try:
								response = get("https://api.codebazan.ir/bio/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("دیالوگ"):
							try:
								response = get("http://api.codebazan.ir/dialog/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "متاسفانه تو ارسال مشکلی پیش اومد!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("دانستنی"):
							try:
								response = get("http://api.codebazan.ir/danestani/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("پ ن پ") or msg.get("text").startswith("!pa-na-pa") or msg.get("text").startswith("په نه په"):
							try:
								response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "شرمنده نتونستم بفرستم!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("الکی مثلا") or msg.get("text").startswith("!alaki-masalan"):
							try:
								response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "نشد بفرستم:(", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("داستان") or msg.get("text").startswith("!dastan"):
							try:
								response = get("http://api.codebazan.ir/dastan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "مشکلی پیش اومد!", message_id=msg["message_id"])
								
						
							
						elif msg.get("text").startswith("پینگ"):
							try:
								responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("gavanin.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
							
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("gavanin.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "✅  قوانین بروزرسانی شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg.get("text") == "حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 10
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "صحبت" or msg.get("text") == "speak" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'پیام شما متن یا کپشن ندارد',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "برداشتن حالت آرام" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "لطفا دستور رو صحیح وارد کنید!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "روشن" or msg.get("text") == "/start" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت روشن شد!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"‼️ کاربر {user} با موفقیت از گروه حذف شد .", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"کاربر {user} شما در زمان {time.localtime().tm_sec} : {time.localtime().tm_min} : {time.localtime().tm_hour} و در تاریخ {time.localtime().tm_mday} / {time.localtime().tm_mon} / {time.localtime().tm_year} به گـروه {name} اضافه شدی \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\n", message_id=msg["message_id"])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"کاربر {user} در تاریخ {time.localtime().tm_mday} / {time.localtime().tm_mon} / {time.localtime().tm_year} از گروه رفت ", message_id=msg["message_id"])
						except:
							print("err Leave member Answer")

							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"هــای {user} عزیز 😘🌹 \n • به گـروه {name} خیـلی خوش اومدی 😍❤️ \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\n", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue

asyncio.run(main())
