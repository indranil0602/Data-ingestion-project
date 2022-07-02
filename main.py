# import required libraries

from datetime import datetime

# import google cloud library

today_date = datetime.now().strftime("%Y-%m-%d")
bucket_name = "data-injection-bucket-gcs-" + today_date
print(bucket_name)

# bucket_name = "your-new-bucket-name"


# check wheather bucket has been created or not


# hit url using api and get response

# store response into bucket

# entry-point function

