
import re


class SuspiciousChecker:

    stringsCausingSuspicions = [

        # php specific
        ";$GLOBALS['",
        "){eval($",
        'eval(base64_decode',

        # js specific
        "CreateObject('WScript.Shell')",
        ' = "cmd.exe /c',
        re.compile('var ([a-z]{60,100}) = \['),  # very long variables, only lowercase
        'Scripting.FileSystemObjectScripting.FileSystemObjectScripting.FileSystemObjectScripting.FileSystemObjectScripting.FileSystemObject',
        'eval(e.responseText.split('
    ]

    def is_file_containing_malicious_content(self, content: str, file_name: str):
        """ Check if file contents contains potentially malicious scripts """

        for suspicious_string in self.stringsCausingSuspicions:
            # if it's a regexp
            if str(suspicious_string.__class__) == "<class '_sre.SRE_Pattern'>":
                if len(suspicious_string.findall(content)) > 0:
                    return True

                continue

            # regular, simple string check
            if suspicious_string in content:
                return True

        return False
