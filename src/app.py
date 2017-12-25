import imaplib
import smtplib
import email
import os
import time


class Post(object):
    """ Post service. """

    IMAP_HOST = None
    SMTP_HOST = None

    IMAP_PORT = 993
    SMTP_PORT = 587

    def __new__(cls, *args, **kwargs):

        if (not cls.IMAP_HOST) or (not cls.SMTP_HOST):
            raise ValueError("IMAP_HOST and SMTP_HOST must be specified or overridden")
        else:
            return super(Post, cls).__new__(cls)

    def __init__(self, login, password):

        self.login = login
        self.password = password

        self.imap = None
        self.smtp = None

    def imap_start(self):
        """
        Starts IMAP session and login.
        :return:
        """

        imap = imaplib.IMAP4_SSL(self.IMAP_HOST, self.IMAP_PORT)
        imap.login(self.login, self.password)

        self.imap = imap

    def imap_close(self):
        """
        Closes IMAP session.
        :return:
        """

        self.imap.close()
        self.imap.logout()

        self.imap = None

    def smtp_start(self):
        """
        Starts SMTP session and login.
        :return:
        """

        smtp = smtplib.SMTP(self.SMTP_HOST, self.SMTP_PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(self.login, self.password)

        self.smtp = smtp

    def smtp_close(self):
        """
        Closes SMTP session.
        :return:
        """

        self.smtp.quit()

        self.smtp = None

    def check_imap(self):
        """
        Checks IMAP session.
        :return:
        """

        if not self.imap:
            if self.smtp:
                self.smtp_close()
            self.imap_start()

    def check_smtp(self):
        """
        Checks SMTP session.
        :return:
        """

        if not self.smtp:
            if self.imap:
                self.imap_close()
            self.smtp_start()

    def get_id(self, folder, sign):
        """
        Gets all id of messages by specific sign.
        :param folder: the folder where messages will be searched
        :param sign: the sign the messages will be searched on
        :return:
        """

        self.imap.select(folder)

        _, msg_ids = self.imap.search(None, sign)
        ids = [int(msg_id) for msg_id in msg_ids[0].split()]

        return ids

    def send(self, recipient, subject, body):
        """
        Sends the message.
        :param recipient: the message recipient
        :param subject: the message subject
        :param body: the message body
        :return:
        """

        self.check_smtp()

        mail = "From: {}\nSubject: {}\nTo: {}\nMIME-Version: 1.0\nContent-Type: text/html\n\n{}".format(
            self.login, subject, recipient, body)

        self.smtp.sendmail(self.login, recipient, mail)

    def forward(self, folder, sign, recipient):
        """
        Forwards the messages to the specified recipient.
        :param folder: the folder the messages will be forwarded from
        :param sign: the sign the messages will be searched on
        :param recipient: the messages recipient
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        self.imap.select(folder)

        for msg_id in ids:

            status, data = self.imap.fetch(msg_id, "(RFC822)")
            email_data = data[0][1]

            mail = email.message_from_string(email_data)
            mail.replace_header("From", self.login)
            mail.replace_header("To", recipient)

            self.check_smtp()

            self.smtp.sendmail(self.login, recipient, mail.as_string())

    def save_body(self, folder, sign, local_directory):
        """
        Saves the message body.
        :param folder: the folder the message body will be saved from
        :param sign: the sign the messages will be searched on
        :param local_directory: the local directory name where the message body will be saved
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        self.imap.select(folder)

        for msg_id in ids:

            status, data = self.imap.fetch(msg_id, "(RFC822)")
            email_data = data[0][1]

            mail = email.message_from_string(email_data)

            date = mail.get("Date")
            h = email.Header.decode_header(date)
            date = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]

            sender = mail.get("From")
            h = email.Header.decode_header(sender)
            sender = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]

            subject = mail.get("Subject")
            h = email.Header.decode_header(subject)
            subject = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]

            body = ""
            for part in mail.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)

            message = "Date: {}\nFrom: {}\nSubject: {}\nBody:\n {}".format(date, sender, subject, body)

            file_name = time.strftime("mail_%d-%m-%Y_%H-%M-%S.txt")
            file_path = os.path.join(local_directory, file_name)

            with open(file_path, "w") as f:
                f.write(message)

    def save_attachments(self, folder, sign, local_directory):
        """
        Saves the message attachments.
        :param folder: the folder the message attachments will be saved from
        :param sign: the sign the messages will be searched on
        :param local_directory: the local directory name where the attachments will be saved
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        self.imap.select(folder)

        for msg_id in ids:

            status, data = self.imap.fetch(msg_id, "(RFC822)")
            email_data = data[0][1]

            mail = email.message_from_string(email_data)

            for part in mail.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                if part.get("Content-Disposition") is None:
                    continue

                attachment = part.get_payload(decode=True)

                file_name = part.get_filename()
                h = email.Header.decode_header(file_name)
                file_name = h[0][0].decode(h[0][1]) if h[0][1] else h[0][0]

                file_path = os.path.join(local_directory, file_name)

                with open(file_path, "wb") as f:
                    f.write(attachment)


class Gmail(Post):
    """ Gmail service. """

    IMAP_HOST = "imap.gmail.com"
    SMTP_HOST = "smtp.gmail.com"

    def __init__(self, login, password):
        super(Gmail, self).__init__(login, password)

    def move(self, folder, sign, label):
        """
        Moves the messages to another folder.
        :param folder: the folder the messages will be moved from
        :param sign: the sign the messages will be searched on
        :param label: the label that will be assigned to messages
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        for msg_id in ids:
            self.imap.store(msg_id, "+X-GM-LABELS", label)

        self.imap.expunge()

    def restore(self, sign):
        """
        Restores the messages from Spam folder to Inbox.
        :param sign: the sign the messages will be searched on
        :return:
        """

        folder = "[Gmail]/&BCEEPwQwBDw-"  # TODO: change to "[Gmail]/Spam"
        label = "\\Inbox"

        self.move(folder, sign, label)


class Yahoo(Post):
    """ Yahoo service. """

    IMAP_HOST = "imap.mail.yahoo.com"
    SMTP_HOST = "smtp.mail.yahoo.com"

    def __init__(self, login, password):
        super(Yahoo, self).__init__(login, password)

    def move(self, folder, folder_to, sign, flag):
        """
        Moves the messages to another folder.
        :param folder: the folder the messages will be moved from
        :param folder_to: the folder the messages will be moved to
        :param sign: the sign the messages will be searched on
        :param flag: the flag that will be assigned to messages
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        for msg_id in ids:
            self.imap.copy(msg_id, folder_to)
            self.imap.store(msg_id, "+FLAGS", flag)

        self.imap.expunge()

    def restore(self, sign):
        """
        Restores the messages from Spam folder to Inbox.
        :param sign: the sign the messages will be searched on
        :return:
        """

        folder = "Bulk Mail"
        folder_to = "INBOX"
        flag = "\\Deleted"

        self.move(folder, folder_to, sign, flag)


class Outlook(Post):
    """ Outlook service. """

    IMAP_HOST = "imap-mail.outlook.com"
    SMTP_HOST = "smtp-mail.outlook.com"

    def __init__(self, login, password):
        super(Outlook, self).__init__(login, password)

    def move(self, folder, folder_to, sign, flag):
        """
        Moves the messages to another folder.
        :param folder: the folder the messages will be moved from
        :param folder_to: the folder the messages will be moved to
        :param sign: the sign the messages will be searched on
        :param flag: the flag that will be assigned to messages
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        for _ in ids:
            self.imap.copy(self.get_id(folder, sign)[-1], folder_to)
            self.imap.store(self.get_id(folder, sign)[-1], "+FLAGS", flag)

        self.imap.expunge()

    def restore(self, sign):
        """
        Restores the messages from Spam folder to Inbox.
        :param sign: the sign the messages will be searched on
        :return:
        """

        folder = "Junk"
        folder_to = "INBOX"
        flag = "\\Deleted"

        self.move(folder, folder_to, sign, flag)


class Aol(Post):
    """ Aol service. """

    IMAP_HOST = "imap.aol.com"
    SMTP_HOST = "smtp.aol.com"

    def __init__(self, login, password):
        super(Aol, self).__init__(login, password)

    def move(self, folder, folder_to, sign, flag):
        """
        Moves the messages to another folder.
        :param folder: the folder the messages will be moved from
        :param folder_to: the folder the messages will be moved to
        :param sign: the sign the messages will be searched on
        :param flag: the flag that will be assigned to messages
        :return:
        """

        self.check_imap()

        ids = self.get_id(folder, sign)

        for msg_id in ids:
            self.imap.copy(msg_id, folder_to)
            self.imap.store(msg_id, "+FLAGS", flag)

        self.imap.expunge()

    def restore(self, sign):
        """
        Restores the messages from Spam folder to Inbox.
        :param sign: the sign the messages will be searched on
        :return:
        """

        folder = "Spam"
        folder_to = "INBOX"
        flag = "\\Deleted"

        self.move(folder, folder_to, sign, flag)
