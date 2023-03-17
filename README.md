# quick-self
👾 Frameworks : Django, Javascript <br>
👉🏻 Link : [http://quickself.kr/](http://quickself.kr/)<br><br>

### Description
This is a quick-self service for easy fuel payment.<br><br>

### List pages

![1](https://user-images.githubusercontent.com/81296203/221506714-3849f8b8-d8e7-4ca9-8e32-93e7bbfd5b43.png) |![2](https://user-images.githubusercontent.com/81296203/221506755-c64ca3ee-c1ca-43ab-8219-698acb762958.png) |![3](https://user-images.githubusercontent.com/81296203/221506758-9e47624f-1296-459a-8594-5c56b58d58a0.png) |![4](https://user-images.githubusercontent.com/81296203/221506759-0279d67e-9630-47bd-8e0e-0b2a7b151a82.png)
--- | --- | --- | --- | 


|url|contents|app|
|------|---|---|
|/|index|app : **users**|
|/enroll/|card view|app : **cards**|
|/enroll/insert|card enroll|app : **cards**|
|/register/|signup|app : **users**|
|/logout/|signout|app : **users**|

<br>

### List of APIs for external.
IP registration is required.

|url|contents|
|------|---|
|/api/v1/receive-cards|Registration for first-time|
|/api/v1/send-card-info|Inquiry of quickself history|

**======> Response messages**<br>
- Success(If successful)
- Failed(If failed)
- Bad Request(Non-POST request)"<br><br>
	
### List of necessaries
- naver_cloud_sens.json (SMS auth)
- secrets.json (Django secretkey)
- socket_port.json (Socket communication IP and host)

<br>
