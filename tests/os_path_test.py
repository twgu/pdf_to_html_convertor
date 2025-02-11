import os

str1: str = 'asdf'
str2: str = 'qwer'
str3: str = '123456////'
str4: str = 'pqpqpqp/'
str5: str = 'mmmm2222'
file_name: str = '계약서'
file_extension: str = '.pdf'

print(
    os.path.join(str1, str2, str3, str4, str5, file_name + file_extension)
)

print(
    os.path.normpath(os.path.join(str1, str2, str3, str4, str5, file_name + file_extension))
)
