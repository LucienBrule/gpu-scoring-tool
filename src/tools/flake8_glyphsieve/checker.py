from ast import AST
from .rules.gls001_pathbased import PathBasedResourceRule
from .rules.gls002_dictload import DictReturnInLoadRule
from .rules.gls003_model_locations import ModelOutsideModelsRule
from .rules.gls004_no_direct_resource_imports import NoDirectResourceImportRule
from .rules.gls005_filesystem_resource_path_violation import FilesystemResourcePathViolationRule


class GlyphSieveChecker:
    def __init__(self, tree: AST, filename: str):
        self.tree = tree
        self.filename = filename

    def run(self):
        rules = [
            PathBasedResourceRule(self.tree, self.filename),
            DictReturnInLoadRule(self.tree, self.filename),
            ModelOutsideModelsRule(self.tree, self.filename),
            NoDirectResourceImportRule(self.tree, self.filename),
            FilesystemResourcePathViolationRule(self.tree, self.filename),
        ]
        for rule in rules:
            yield from rule.run()
