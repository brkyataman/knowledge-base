from GeniaTaggerClient import GeniaTaggerClient


print("started")
tagger = GeniaTaggerClient()
while True:
    userInput = input("give ur input: ")
    if userInput == "e":
        break
    tagger.send_message(userInput)

print("le finish")
