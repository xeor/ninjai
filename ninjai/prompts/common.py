from ninjai import PromptHandler

class GenericPrompt(PromptHandler):
    def prompt(self):
        prompt = ''
        prompt += r'{color.LightGreen}\u@\h' # Hostname
        prompt += r'{color.LightBlue}[{color.LightCyan}\Y1{color.LightBlue}]' # Path
        prompt += r'{color.Green}|\#> '
        return prompt

