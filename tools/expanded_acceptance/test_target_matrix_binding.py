import unittest
from target_matrix_binding import SOURCE, PATH, target_matrix_table_pointer


class TargetMatrixBindingTests(unittest.TestCase):
    def setUp(self):
        self.b = dict(path=PATH, pointer='/satellite_host_ratings/comsats/acifs')
        self.f = {'class': 'rule_exact', 'kind': 'row'}
        self.p = dict(printed=116, pdf=117)

    def check(self, b=None, f=None, s=None, p=None):
        return target_matrix_table_pointer(self.b if b is None else b, self.f if f is None else f,
                                           SOURCE if s is None else s, self.p if p is None else p)

    def test_four_tables(self):
        for n, pointer in [(116, self.b['pointer']), (117, '/doj/search_modifiers/FBI'),
                           (118, '/magicknet/threshold_guardian/stats/utilities/Armor'),
                           (119, '/shiawase_mifd/semi_autonomous_knowbots/utilities/Track_sensitive')]:
            self.assertTrue(self.check(b=dict(self.b, pointer=pointer), p=dict(printed=n, pdf=n+1)))

    def test_wrong_source_identity(self):
        for k in SOURCE:
            self.assertFalse(self.check(s=dict(SOURCE, **{k: None})))

    def test_wrong_page(self):
        for p in (dict(printed=117, pdf=118), dict(printed=116, pdf=116), dict(printed=116.0, pdf=117), {}):
            self.assertFalse(self.check(p=p))

    def test_wrong_path_mode_class_kind(self):
        self.assertFalse(self.check(b=dict(self.b, path='rules/matrix/other.yml')))
        self.assertFalse(self.check(b=dict(self.b, mode='sr3-accepted-core-equivalence/v1')))
        self.assertFalse(self.check(f=dict(self.f, **{'class':'equipment_stat'})))
        self.assertFalse(self.check(f=dict(self.f, kind='condition')))

    def test_no_root_or_unreviewed_descendants(self):
        for ptr in ('/headline', '/summary', '/satellite_host_ratings', '/satellite_host_ratings/comsats',
                    '/satellite_host_ratings/comsats/acifs/0', '/satellite_host_ratings/comsats/fake',
                    '/satellite_host_ratings/comsats/acifs\n', '/doj/offline_archive'):
            self.assertFalse(self.check(b=dict(self.b, pointer=ptr)))

    def test_table_specific_columns(self):
        for ptr in ('/shiawase_mifd/smart_frames/hacking_pool', '/shiawase_mifd/agents/utility_pool',
                    '/shiawase_mifd/semi_autonomous_knowbots/utilities/Browse_sensitive'):
            self.assertFalse(self.check(b=dict(self.b, pointer=ptr), p=dict(printed=119, pdf=120)))


if __name__ == '__main__':
    unittest.main()
