
from evennia.utils import create 
from evennia.utils.test_resources import BaseEvenniaTest 

from module import utils

class TestUtils(BaseEvenniaTest):
    def test_get_obj_stats(self):
        # make a simple object to test with 
        obj = create.create_object(
            key="testobj", 
            attributes=(("desc", "A test object"),)
        ) 
        # run it through the function 
        result = utils.get_obj_stats(obj)
        # check that the result is what we expected
        self.assertEqual(
            result,
            """
|ctestobj|n
Valeur: ~|y10|n C$ [Pas porté]

A test object

Taille: |w1|n, Used from: |wSac à dos|n
État: |w3|n, Utilisation: |winfinie|n
Attacks using |wForce|n contre |wArmure|n
Dé de dégâts: |w1d6|n
""".strip()
)