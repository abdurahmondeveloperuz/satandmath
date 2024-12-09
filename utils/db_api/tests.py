from sqlite import Database, TestManager


def test():
    # # Users Database
    # db = Database(path_to_db='test.db')
    # db.create_table_users()
    # db.add_user(1, "One", "email", 'ru')
    # db.add_user(2, "olim", "olim@gmail.com", 'uz')
    # db.add_user(3, 1, 1)
    # db.add_user(4, 1, 1)
    # db.add_user(5, "John", "john@mail.com")

    # users = db.select_all_users()
    # print(f"Barcha fodyalanuvchilar: {users}")

    # user = db.select_user(Name="John", id=5)
    # print(f"Bitta foydalanuvchini ko'rish: {user}")

    # # Test Manager
    manager = TestManager()

    test_id = manager.save_test("ABCDABCDABCD", 54654)
    print(f"Test ID: {test_id}")

    result = manager.check_test(test_id, "DGSJDKEOAS")
    print(result)

    manager.end_test(test_id)

    status = manager.check_status(test_id)
    print(f"Test status: {status}")

test()
