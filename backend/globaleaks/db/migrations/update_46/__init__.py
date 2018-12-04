# -*- coding: UTF-8
from globaleaks.db.migrations.update import MigrationBase


class MigrationScript(MigrationBase):
    def epilogue(self):
        tenants = self.session_new.query(self.model_from['Tenant'])
        for t in tenants:
            m = self.model_from['Config']
            a = self.session_new.query(m.value).filter(m.tid == t.id, m.var_name == u'ip_filter_authenticated_enable').one()[0]
            b = self.session_new.query(m.value).filter(m.tid == t.id, m.var_name == u'ip_filter_authenticated').one()[0]

            for c in ['admin', 'custodian', 'receiver']:
                self.session_new.add(self.model_to['Config'](t.id, u'ip_filter_' + c + '_enable', a))
                self.session_new.add(self.model_to['Config'](t.id, u'ip_filter_' + c, b))
                self.entries_count['Config'] += 2
