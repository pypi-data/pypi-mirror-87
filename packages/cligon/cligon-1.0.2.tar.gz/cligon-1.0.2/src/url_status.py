"""class for url statuses"""
try:
    from src import terminal_colors
except ModuleNotFoundError:
    import terminal_colors

TerminalColors = terminal_colors.TerminalColors


class UrlStatus:
    """to collect status of URLs"""

    def __init__(self, link, result, code):
        """init"""
        self.link = link
        self.result = result
        self.code = code

    def get_result_name(self):
        """return result"""
        return self.result

    def get_status_code(self):
        """return status code"""
        return self.code

    def color(self):
        """colorize the URLs by status"""
        if self.result == "BAD":
            return TerminalColors.RED
        if self.result == "GOOD":
            return TerminalColors.GREEN

        return TerminalColors.GREY

    def output(self, args):
        """out put url_status"""
        if args.json:
            return '{ "url": "' + self.link + '", "status": "' + str(self.code) + '" }'

        return (
            self.color()
            + f"{self.result:7}"
            + TerminalColors.ENDCOLOR
            + " -> "
            + self.color()
            + self.link
            + TerminalColors.ENDCOLOR
        )
