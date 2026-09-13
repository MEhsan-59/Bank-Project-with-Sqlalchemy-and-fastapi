def test_admin_authentication(admin_manager):

    status, msg = admin_manager.check_admin("hi", "h1")
    assert status is True
    assert msg == "Admin authenticated successfully."

    status, msg = admin_manager.check_admin("hi", "wrongpassword")
    assert status is False
    assert msg == "Invalid admin ID or password."

    status, msg = admin_manager.check_admin("", "")
    assert status is False
    assert msg == "Admin ID and password cannot be empty."

def test_admin_authentication_not_found(admin_manager):
    status, msg = admin_manager.check_admin("nonexistent", "password")
    assert status is False
    assert msg == "Invalid admin ID or password."

def test_admin_authentication_empty_fields(admin_manager):
    status, msg = admin_manager.check_admin("", "")
    assert status is False
    assert msg == "Admin ID and password cannot be empty."
