import re


class StringValidator(str):
    pattern = None

    def isvalid(self):
        if not self.pattern:
            return True
        return bool(re.match(pattern=self.pattern, string=self))

    def __repr__(self):
        return self.replace("&", '&amp;')
