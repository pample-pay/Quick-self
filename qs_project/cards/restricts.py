def form_card_num_valid(ccf):

    num1 = ccf['card_num1']
    num2 = ccf['card_num2']
    num3 = ccf['card_num3']
    num4 = ccf['card_num4']
    
    # 각 입력 버튼의 길이
    if len(num1)!=4 or len(num2)!=4 or len(num3)!=4 or len(num4)!=4:
        return False
    
    # 모두 숫자인지 확인
    if (num1.isdigit() and num2.isdigit() and num3.isdigit() and num4.isdigit()) != True:
        return False

    # 카드번호 자리수 알고리즘
    if card_valid_algo(num1+num2+num3+num4) != True:
        return False
    
    return True


def point_valid(ccf):
    num1 = ccf['point_num1']
    num2 = ccf['point_num2']
    num3 = ccf['point_num3']
    num4 = ccf['point_num4']

    # 각 입력 버튼의 길이
    if len(num1)!=4 or len(num2)!=4 or len(num3)!=4 or len(num4)!=4:
        return False
    
    #모두 숫자인지 확인
    if (num1.isdigit() and num2.isdigit() and num3.isdigit() and num4.isdigit()) != True:
        return False

    return True
    

def card_nickname(cw, cn1):

    if cw == '0' : card_init = '국민'
    elif cw == '1' : card_init = '삼성'
    elif cw == '2' : card_init = '신한'
    elif cw == '3' : card_init = '우리'
    elif cw == '4' : card_init = '하나'
    elif cw == '5' : card_init = '롯데'
    elif cw == '6' : card_init = '현대'
    elif cw == '7' : card_init = '농협'
    elif cw == '8' : card_init = 'IBK'
    elif cw == '9' : card_init = '카카오'
    elif cw == '10' : card_init = '토스'

    cn = card_init + cn1

    return cn


def card_valid_algo(card_num):

    vn = 0

    for i in range(15):
        vn += (int(card_num[i])*(2-i%2)) if int(card_num[i])*(2-i%2)<10 else (int(card_num[i])*(2-i%2)//10+int(card_num[i])*(2-i%2)%10)

    if (vn + int(card_num[15])) % 10 == 0:
        return True
    else:
        return False

