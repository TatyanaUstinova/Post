from app import Aol

LOGIN = "ustinova.tatyana@aol.com"
PASSWORD = "****"

# FOLDER = "INBOX"
FOLDER = "Spam"

FOLDER_TO = "INBOX"

FLAG = "\\Deleted"

SIGN = '(FROM "ustinova.tatyana.s@gmail.com")'
# SIGN = '(SUBJECT "document-scanner.zip")'
# SIGN = '(SUBJECT "inventions.docx, rossum.jpg")'
# SIGN = '(SUBJECT "test")'

RECIPIENT = "ustinova.tatyana.s@mail.ru"
SUBJECT = "python"
BODY = "Hello!"

# LOCAL_DIRECTORY = "mail"
LOCAL_DIRECTORY = "d:\\dev\\programming\\work\\post\\src\\mail"


if __name__ == "__main__":

    aol = Aol(LOGIN, PASSWORD)

    # ---------- MOVE ----------
    aol.check_imap()

    ids = aol.get_id(FOLDER, SIGN)
    print ids

    aol.move(FOLDER, FOLDER_TO, SIGN, FLAG)

    ids = aol.get_id(FOLDER, SIGN)
    print ids

    # ---------- RESTORE ----------
    aol.restore(SIGN)
    ids = aol.get_id(FOLDER, SIGN)
    print ids

    # ---------- SEND ----------
    aol.send(RECIPIENT, SUBJECT, BODY)

    # ---------- FORWARD ----------
    aol.forward(FOLDER, SIGN, RECIPIENT)

    # ---------- SAVE BODY ----------
    aol.save_body(FOLDER, SIGN, LOCAL_DIRECTORY)
    #
    # ---------- SAVE ATTACHMENTS ----------
    aol.save_attachments(FOLDER, SIGN, LOCAL_DIRECTORY)
