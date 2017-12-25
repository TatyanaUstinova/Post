from app import Yahoo

LOGIN = "ustinova.tatyana@yahoo.com"
PASSWORD = "****"

# FOLDER = "INBOX"
FOLDER = "Bulk Mail"

FOLDER_TO = "INBOX"

FLAG = "\\Deleted"

# SIGN = '(FROM "ustinova.tatyana.s@gmail.com")'
# SIGN = '(SUBJECT "01-banksy-wallpaper.jpg")'
# SIGN = '(SUBJECT "test")'
SIGN = "UNSEEN"
# SIGN = "SEEN"

RECIPIENT = "ustinova.tatyana.s@mail.ru"
SUBJECT = "python"
BODY = "Hello!"

# LOCAL_DIRECTORY = "mail"
LOCAL_DIRECTORY = "d:\\dev\\programming\\work\\post\\src\\mail"


if __name__ == "__main__":

    yahoo = Yahoo(LOGIN, PASSWORD)

    # ---------- MOVE ----------
    yahoo.check_imap()

    ids = yahoo.get_id(FOLDER, SIGN)
    print ids

    yahoo.move(FOLDER, FOLDER_TO, SIGN, FLAG)

    ids = yahoo.get_id(FOLDER, SIGN)
    print ids

    # ---------- RESTORE ----------
    yahoo.restore(SIGN)

    # ---------- SEND ----------
    yahoo.send(RECIPIENT, SUBJECT, BODY)
    #
    # ---------- FORWARD ----------
    yahoo.forward(FOLDER, SIGN, RECIPIENT)

    # ---------- SAVE BODY ----------
    yahoo.save_body(FOLDER, SIGN, LOCAL_DIRECTORY)
    #
    # ---------- SAVE ATTACHMENTS ----------
    yahoo.save_attachments(FOLDER, SIGN, LOCAL_DIRECTORY)
