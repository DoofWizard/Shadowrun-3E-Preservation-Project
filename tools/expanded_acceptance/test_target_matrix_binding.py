import unittest
from target_matrix_binding import SOURCE, PATH, PERSONA_PATH, target_matrix_table_pointer


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

    def test_exact_original_persona_rating_pairs(self):
        expected = [(126, 'anubis'), (126, 'fastjack'), (126, 'grid_reaper'),
                    (127, 'link'), (127, 'red_wraith'), (128, 'silvery_k'),
                    (128, 'slamm_0'), (128, 'smiling_bandit'), (128, 'snow_tiger'),
                    (129, 'michael_sutherland')]
        for page, name in expected:
            with self.subTest(page=page, name=name):
                b = dict(path=PERSONA_PATH, pointer=f'/ratings/{name}/npc_ratings')
                p = dict(printed=page, pdf=page+1)
                self.assertTrue(self.check(b=b, p=p))
                self.assertFalse(self.check(b=b, p=dict(printed=page+1, pdf=page+2)))
                self.assertFalse(self.check(b=b, p=dict(printed=page, pdf=page)))
                self.assertFalse(self.check(b=dict(b, path=PATH), p=p))
                self.assertFalse(self.check(b=b, f=dict(self.f, kind='condition'), p=p))
                self.assertFalse(self.check(b=b, f=dict(self.f, **{'class':'equipment_stat'}), p=p))
                self.assertFalse(self.check(b=b, s=dict(SOURCE, edition='SR2'), p=p))

    def test_persona_unreviewed_root_paths_rejected(self):
        for pointer in ('/ratings', '/ratings/anubis', '/ratings/anubis/npc_ratings/0',
                        '/ratings/anubis/npc_ratings\n', '/ratings/anubis/exceptional_skills',
                        '/ratings/new_npc/npc_ratings', '/headline', '/summary'):
            self.assertFalse(self.check(b=dict(path=PERSONA_PATH, pointer=pointer),
                                        p=dict(printed=126, pdf=127)))


if __name__ == '__main__':
    unittest.main()
