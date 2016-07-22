import sqllib
try:
    sqllib.DefineUserTable()
    print("UserTable created")
except Exception as e:
    print(e)
try:
    sqllib.DefineArticalTable()
    print("ArticalTable created")
except Exception as e:
    print(e)
try:
    sqllib.DefineArticalSearchTable()
    print("ArticalSearchTable created")
except Exception as e:
    print(e)
import test
try:
    test.TestFastCreateUser()
    print("TestFastCreateUser")
except Exception as e:
    print(e)
try:
    test.TestFastCreatArtical()
    print("TestFastCreatArtical")
except Exception as e:
    print(e)