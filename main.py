from python.TextInputHandler import TextInputHandler


def main():
    # Beispiel für den Start der Ausführung
    input_text = input("Bitte geben Sie Ihre Anweisung ein: ")
    text_handler = TextInputHandler()
    command = text_handler.handle_input(input_text)

    # Hier würde die Logik zur Verarbeitung der Anweisung folgen
    print(f"Instruction received: {command}")

if __name__ == "__main__":
    main()
