class NamespaceTranslator():
  def __init__(self, separator, pathAliases):
    self.separator = separator
    self.pathAliases = pathAliases

class NamespaceTranslatorBuilder():
  def __init__(self):
    self.separator = '.'
    self.pathAliases = []
  def withSeparator(self, sep):
    self.separator = sep
    return self
  def withPathAlias(self, pathAlias):
    self.pathAliases.append(pathAlias)
    return self
  def build(self):
    return NamespaceTranslator(self.separator, self.pathAliases)