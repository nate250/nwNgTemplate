import unittest
import mock
from lib.NamespaceTranslator import *

class TestNamespaceTranslator(unittest.TestCase):
  def test_testing(self):
    self.assertEqual(1,1);

class TestNamespaceTranslatorBuilder(unittest.TestCase):
  def test_buildReturnsNamespaceTranslator(self):
    builder = NamespaceTranslatorBuilder()
    self.assertIsInstance(builder.build(), NamespaceTranslator)

  def test_buildWithSeparator(self):
    translator = NamespaceTranslatorBuilder().withSeparator('-').build()
    self.assertEqual(translator.separator, '-')

  def test_buildWithPathAlias(self):
    translator = NamespaceTranslatorBuilder().withPathAlias({'as/df': 'fd-sa'}).build()
    self.assertEqual(translator.pathAliases, [{'as/df': 'fd-sa'}])

  def test_buildWithMultiplePathAliases(self):
    translator = NamespaceTranslatorBuilder() \
                 .withPathAlias({'as/df': 'fd-sa'}) \
                 .withPathAlias({'ab/cd': 'cd-ab'}) \
                 .build()
    self.assertEqual(translator.pathAliases, [{'as/df': 'fd-sa'},{'ab/cd': 'cd-ab'}])