# -*- coding: utf-8 -*-
# from cpskin.policy.testing import CPSKIN_POLICY_ROBOT_TESTING
# from plone.testing import layered
# import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    # suite.addTests([
    #     layered(robotsuite.RobotTestSuite('robot'),
    #             layer=CPSKIN_POLICY_ROBOT_TESTING),
    # ])
    return suite
