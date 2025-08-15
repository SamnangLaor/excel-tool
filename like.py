import autolike

url = "https://www.facebook.com/share/r/1BUo8JvVEL/" # any Facebook URL
run_time = 30 # time in seconds
like_result_dict = autolike.facebook_autolike(url, run_time)
print(like_result_dict)