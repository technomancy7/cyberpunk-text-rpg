class JEGUI:
    def push_dialog(self, speaker, message):
        self.dialog_stack.append([speaker, message])

    def log(self, txt):
        iters = 0
        # Send a message to the in-game terminal
        print(len(txt), "<", self.log_size_limit, "=", len(txt) <= self.log_size_limit)
        if len(txt) < self.log_size_limit:
            self.msg_history.append(txt)
            self.msg_history_proxy.append("")
        else:
            out = []
            while len(txt) >= self.log_size_limit:
                iters += 1
                newsplit = " ".join(txt[0:self.log_size_limit].split(" ")[:-1])
                txt = txt[len(newsplit):]
                self.msg_history.append(newsplit)
                self.msg_history_proxy.append("")
                if iters > 10:
                    print("EMERGENCY BREAK: Log message too big.")
                    break

            self.msg_history.append(txt)
            self.msg_history_proxy.append("")

    def refresh_text_input(self):
        # Refreshes the string of text used for the terminal input
        self.text_input_ln = "".join(self.text_buffer)

    def proceed_dialog(self):
        if len(self.dialog_stack) > 0:
            if self.dialog_msg_proxy != self.dialog_stack[0][1]:
                self.dialog_msg_proxy = self.dialog_stack[0][1]
            else:
                self.dialog_stack.remove(self.dialog_stack[0])
                self.dialog_msg_proxy = ""   
            return True
        return False