# -*- coding: utf-8 -*-
def testSetup(context):
    if context.readDataFile('imio.media.txt') is None:
        return
