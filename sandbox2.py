import datetime

now = datetime.datetime.now()
now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
print(now_str)
