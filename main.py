from GeniaTaggerClient import GeniaTaggerClient


print("started")
tagger = GeniaTaggerClient()
while True:
    userInput = input("give ur input: \n")
    if userInput == "e":
        break
    elif userInput == "s":
        tagger.print_pos_tags()
    else:
        tagger.send_message(userInput)

print("le finish")
