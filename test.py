def myfind(x,y):
    return [ a for a in range(len(y)) if y[a] == x]

a='4abbe5b7-a00d-4a82-b3d8-fe851bba80fe|中国农业发展银行乾安县支行与上海儒仕实业有限公司、江苏索普（集团）有限公司合同纠纷二审民事裁定书|2015-07-24'

index=myfind("|",a)
print(index)
print(a[37:85])