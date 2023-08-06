from revns.django import EmailNotification as EmailNtfn, SmsNotification as SmsNtfn


class CodeEmailNtfn(EmailNtfn):
    def build_target(self):
        return self.instance.identity

    def build_title(self):
        return 'REVAUTH VALIDATION'

    def build_body(self):
        code = self.instance.code
        return code


class CodeSmsNtfn(SmsNtfn):
    def build_target(self):
        return self.instance.identity

    def build_title(self):
        return 'REVAUTH VALIDATION'

    def build_body(self):
        return self.instance.code
