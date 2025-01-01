from ssg1 import format_filename, has_alphanumeric, GENERATED_FILENAMES

def test_has_alphanumeric():
    assert has_alphanumeric("Hello123") == True
    assert has_alphanumeric("@#$%^") == False
    assert has_alphanumeric("") == False

def test_normal_cases():
    print("Testing normal cases:")
    print(format_filename("Exploring Python Decorators!!!"))
    print(format_filename("Hello World"))

def test_edge_cases():
    print("\nTesting edge cases:")
    print(format_filename(""))  # empty string
    print(format_filename("   "))  # just spaces

def test_windows_reserved():
    print("\nTesting Windows reserved names:")
    print(format_filename("COM2"))
    print(format_filename("PRN.html"))

def test_long_filenames():
    print("\nTesting very long filenames:")
    very_long = "Exploring Python Decorators!!!" * 8
    print(format_filename(very_long))

def test_collision_tracking():
    print("\nTesting collision tracking:")
    print(format_filename(""))  # should generate unique name
    print(format_filename(""))  # should generate different unique name
    print("Generated filenames:", GENERATED_FILENAMES)

if __name__ == "__main__":
    test_normal_cases()
    test_edge_cases()
    test_windows_reserved()
    test_long_filenames()
    test_collision_tracking()
    test_has_alphanumeric()