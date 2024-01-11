from xmlrpc import client


class ApiHelper:
    def __init__(self, url: str, port: str, db_name: str, username: str, password: str):
        self.url = url
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self.uid, self.md = self._db_connection()

    def _db_connection(self):
        port = ":%s" % self.port if self.port else ""
        full_url = "%s%s" % (self.url, port)
        endpoint = "{}/xmlrpc/2/"
        common_endpoint = "%s%s" % (endpoint, "common")
        md_endpoint = "%s%s" % (endpoint, "object")
        common = client.ServerProxy(common_endpoint.format(full_url))
        uid = common.authenticate(self.db_name, self.username, self.password, {})
        md = client.ServerProxy(md_endpoint.format(full_url))

        return [uid, md]

    def get_record_value(self, records, default_value=""):
        return records[1] if records else default_value

    def get_record_key(self, records, default_value=False):
        try:
            return records[0]
        except Exception:
            return default_value

    def get_unique_record_array(self, records, default_value=None):
        return records[0] if records else default_value

    def check_rights(self, model: str, rights: list[str]) -> bool:
        return self.md.execute_kw(
            self.db_name,
            self.uid,
            self.password,
            model,
            "check_access_rights",
            rights,
            {"raise_exception": False},
        )

    def search(self, model: str, domains=[[]]):
        return self.md.execute_kw(
            self.db_name,
            self.uid,
            self.password,
            model,
            "search",
            domains,
        )

    def search_read(self, model: str, fields: list[str], domains=[[]], **kwargs):
        params = {"fields": fields}
        params.update(kwargs)

        return self.md.execute_kw(
            self.db_name,
            self.uid,
            self.password,
            model,
            "search_read",
            domains,
            params,
        )

    def search_count(self, model: str, domains=[[]]):
        return self.md.execute_kw(
            self.db_name, self.uid, self.password, model, "search_count", domains
        )
