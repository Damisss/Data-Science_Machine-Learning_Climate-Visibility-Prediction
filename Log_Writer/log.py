from datetime import datetime

def logWriter(fileObject, message):
    dateInfo = datetime.now()
    date = dateInfo.date()
    currentHour = dateInfo.strftime('%H:%M:%S')
    return fileObject.write(f'{str(date)} | {str(currentHour)} | {message}' + '\n')

