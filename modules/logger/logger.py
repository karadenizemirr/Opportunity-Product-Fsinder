from datetime import datetime

def create_log(data,filename):
    f = open(f"modules/logger/{filename}.txt", "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), data))
    f.close()