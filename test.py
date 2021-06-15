import time

start = input("Enter를 누르면 타이머를 시작합니다.")
time_start= time.time()

sent = "다른모든눈송이와아주비슷하게생긴단하나의눈송이" #문장
typecount = 58 #타자획수

sent_type = input("문장을 입력하세요")
time_stop = time.time() #시간 멈추기
result = time_stop - time_start #걸린시간 계산
print(typecount, result)
result_time = typecount / result * 60 #타자속도 계산

if sent_type == sent:
    print("성공")
    print("타자 속도 : " + str(round(result_time)) + "t")
    print("걸린 시간 : " + str(result))