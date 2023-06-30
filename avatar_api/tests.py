import app

def test_initials():
    assert app.get_name_initials("Abhijeet Sonar") == "AS"
    assert app.get_name_initials("Abhijeet") == "A"
    assert app.get_name_initials("Abc Def Ghi") == "AD"
