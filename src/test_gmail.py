from app import Gmail

LOGIN = "ustinova.tatyana.s@gmail.com"
PASSWORD = "****"

# FOLDER = "INBOX"
FOLDER = "[Gmail]/&BCEEPwQwBDw-"  # "[Gmail]/Spam"

LABEL = "\\Inbox"

SIGN = '(FROM "ustinova.tatyana.s@mail.ru")'
# SIGN = '(SUBJECT "document-scanner.zip")'
# SIGN = '(SUBJECT "inventions.docx, inventions.pptx, NewYork.srt")'
# SIGN = '(SUBJECT "inventions.docx, rossum.jpg")'
# SIGN = '(SUBJECT "test")'

RECIPIENT = "ustinova.tatyana.s@mail.ru"
SUBJECT = "python"
BODY = "Hello!"

# LOCAL_DIRECTORY = "mail"
LOCAL_DIRECTORY = "d:\\dev\\programming\\work\\post\\src\\mail"


if __name__ == "__main__":

    gmail = Gmail(LOGIN, PASSWORD)

    # ---------- MOVE ----------
    gmail.check_imap()

    ids = gmail.get_id(FOLDER, SIGN)
    print ids

    gmail.move(FOLDER, SIGN, LABEL)

    ids = gmail.get_id(FOLDER, SIGN)
    print ids

    # ---------- RESTORE ----------
    gmail.restore(SIGN)

    # ---------- SEND ----------
    gmail.send(RECIPIENT, SUBJECT, BODY)

    # ---------- FORWARD ----------
    gmail.forward(FOLDER, SIGN, RECIPIENT)

    # ---------- SAVE BODY ----------
    gmail.save_body(FOLDER, SIGN, LOCAL_DIRECTORY)
    #
    # ---------- SAVE ATTACHMENTS ----------
    gmail.save_attachments(FOLDER, SIGN, LOCAL_DIRECTORY)
