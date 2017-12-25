from app import Outlook

LOGIN = "ustinova.tatyana@outlook.com"
PASSWORD = "****"

# FOLDER = "INBOX"
FOLDER = "Junk"

FOLDER_TO = "INBOX"

FLAG = "\\Deleted"

# SIGN = '(FROM "ustinova.tatyana.s@mail.ru")'
SIGN = '(FROM "ustinova.tatyana.s@gmail.com")'
# SIGN = '(SUBJECT "test")'
# SIGN = "UNSEEN"
# SIGN = "SEEN"

RECIPIENT = "ustinova.tatyana.s@mail.ru"
SUBJECT = "python"
BODY = "Hello!"

# LOCAL_DIRECTORY = "mail"
LOCAL_DIRECTORY = "d:\\dev\\programming\\work\\post\\src\\mail"


if __name__ == "__main__":

    outlook = Outlook(LOGIN, PASSWORD)

    # ---------- MOVE ----------
    outlook.check_imap()

    ids = outlook.get_id(FOLDER, SIGN)
    print ids

    outlook.move(FOLDER, FOLDER_TO, SIGN, FLAG)

    ids = outlook.get_id(FOLDER, SIGN)
    print ids

    # ---------- RESTORE ----------
    outlook.restore(SIGN)

    # ---------- SEND ----------
    outlook.send(RECIPIENT, SUBJECT, BODY)
    #
    # ---------- FORWARD ----------
    outlook.forward(FOLDER, SIGN, RECIPIENT)

    # ---------- SAVE BODY ----------
    outlook.save_body(FOLDER, SIGN, LOCAL_DIRECTORY)
    #
    # ---------- SAVE ATTACHMENTS ----------
    outlook.save_attachments(FOLDER, SIGN, LOCAL_DIRECTORY)
