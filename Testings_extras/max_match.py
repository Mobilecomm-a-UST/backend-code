def max_match(str1,str2):
    len_f=len(str1)
    len_s=len(str2)

    if len_f > len_s:
        length=len_s
    else:
        length=len_f

    count=0
    for i in range(0,length):
        if str1[i]==str2[i]:
            count=count+1
        else:
            break


    return count

str1="srarmu"
str2="rarbu"
c= max_match(str1,str2)
print(c)

################# project old code ##############

# def max_match(str1,str2):
#     len_f=len(str1)
#     len_s=len(str2)

#     if len_f > len_s:
#         length=len_s
#     else:
#         length=len_f

#     count=0
#     for i in range(0,length):
#         if str1[i]==str2[i]:
#             count=count+1
#         else:
#             break
#     str1=str1.strip()
#     str2=str2.strip()
#     m_sts=False
#     if str1[-1]==str2[-1]:
#            count=count+1
#            m_sts=True

#     return count,m_sts

##########################################################