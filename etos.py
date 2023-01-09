class EternalTerminal:
    def init_etos(self):
        self.virtual_fs = []
        self._etos_new_file(name="system", ftype="dir"),
        self._etos_new_file(name="etos", ftype="dir", location="/system/"),
        self._etos_new_file(name="documents", ftype="dir"),
        self._etos_new_file(name="images", ftype="dir"),
        self._etos_new_file(name="notes", ftype="dir"),
        self._etos_new_file(name="$STATS", ftype="system", location="/system/etos/")
        self._etos_new_file(name="$GOALS", ftype="system", location="/system/etos/")
        self._etos_new_file(name="ETOS_SYS", ftype="system", location="/system/")
        self._etos_new_file(name="WORLD", ftype="system", location="/system/")
        self._etos_new_file(name="SELF", ftype="system", location="/system/")
        self._etos_new_file(name="INTERFACE", ftype="system", location="/system/")
        self._etos_new_file(name="PERCEPTION", ftype="system", location="/system/")
        print(self.virtual_fs)


    @property
    def etos_cwd(self):
        return self.variables.get("cwd", "/")

    @etos_cwd.setter
    def etos_cwd(self, new_cwd):
        self.variables["last_cwd"] = self.variables.get("cwd", "/")
        new_cwd = str(new_cwd)
        if new_cwd == "": new_cwd = "/"
        if not new_cwd.endswith("/"): new_cwd = new_cwd+"/"
        self.variables["cwd"] = new_cwd

    def etos_get_file(self, path):
        for f in self.virtual_fs:
            if f['location']+f['name'] == path:
                return f

        name = path.split("/")[-1]
        path = "/".join(path.split("/")[0:-1])
        return self._etos_new_file(name=name, location=path)

    def etos_writefile(self, path, body):
        f = self.etos_get_file(path)
        f["body"] = body
        return f

    def etos_renamefile(self, old_path, new_path):
        pass

    def etos_delfile(self, path):
        pass
