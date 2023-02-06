def form_card_num_valid(num1:str, num2:str, num3:str, num4:str):
    
    # 각 입력 버튼의 길이
    if len(num1)!=4 or len(num2)!=4 or len(num3)!=4 or len(num4)!=4:
        error = '카드 번호 길이를 확인해 주세요.'
        return error
    
    if (num1.isdigit() and num2.isdigit() and num3.isdigit() and num4.isdigit()) != True:
        error = '카드 번호를 확인해 주세요.'
        return error
    
    return True
    
