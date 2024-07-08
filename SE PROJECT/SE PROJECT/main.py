# Main function
def main():
    new_user = input("Are you a new user? (yes/no): ")
    if new_user.lower() == "yes":
        name = input("Enter your name: ")
        capture_images(name)
    else:
        recognize_and_verify()

    command = input("Do you want to access or enter the website now? (yes/no): ")
    if command.lower() == "yes":
        recognize_and_verify()

if __name__ == "__main__":
    main()
