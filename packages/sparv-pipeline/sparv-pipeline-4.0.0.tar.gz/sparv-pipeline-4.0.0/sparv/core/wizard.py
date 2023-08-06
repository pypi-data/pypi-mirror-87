"""Sparv corpus set-up wizard."""
import os
import re
import sys
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Callable, List, Optional, Tuple, Union

import questionary.prompts.common
import yaml
from prompt_toolkit.shortcuts import clear as clear_screen
from prompt_toolkit.styles import Style
from questionary import prompt

from sparv import SourceStructureParser, Wildcard
from sparv.core import registry, paths, config, snake_utils
from sparv.core.console import console

questionary.prompts.common.SELECTED_POINTER = "\u276f"

style = Style.from_dict({
    "pointer": "#FF9D00 bold",
    "answer": "fg:#FF9D00",
    "question": "nobold",
    "disabled": "fg:#999999"
})

DONE = "✅ DONE"


class BasicSourceStructure(SourceStructureParser):
    """Simple SourceStructureParser implementation which doesn't scan source files."""

    def get_annotations(self, corpus_config: dict) -> List[str]:
        """Return annotations."""
        return self.annotations


class Wizard:
    """A wizard for setting up a corpus config."""

    def __init__(self):
        """Initialize wizard."""
        self.corpus_config = {}  # Dict holding the resulting config structure
        self.here = os.getcwd()
        self.config_file = os.path.join(self.here, paths.config_file)

        # Annotator info
        self.snake_storage = None
        self.output_to_annotators = {}
        self.annotation_to_annotator = {}
        self.annotation_description = {}
        self.wildcard_annotations = []
        self.importers = defaultdict(dict)

        self.source_structure: Optional[SourceStructureParser] = None

    def update_annotators(self):
        """Update storage."""
        self.output_to_annotators = defaultdict(list)
        self.annotation_to_annotator = {}
        self.annotation_description = {}
        registry.annotation_classes["config_classes"] = config.config.get("classes", {})

        if not registry.modules:
            registry.find_modules()

        self.snake_storage = snake_utils.SnakeStorage()

        for module_name in registry.modules:
            for f_name, annotator in registry.modules[module_name].functions.items():
                # Init rule storage
                rule_storage = snake_utils.RuleStorage(module_name, f_name, annotator)

                # Process rule parameters and update rule storage
                rule_made = snake_utils.rule_helper(rule_storage, config.config, self.snake_storage)
                if rule_storage.annotator and self.snake_storage.all_annotators.get(module_name, {}).get(f_name):
                    self.snake_storage.all_annotators[module_name][f_name]["rule"] = rule_storage
                    for output in rule_storage.outputs:
                        self.output_to_annotators[output].append((module_name, f_name))
                    for annotation in self.snake_storage.all_annotators[module_name][f_name]["annotations"]:
                        self.annotation_to_annotator[annotation[0].original_name] = (module_name, f_name)
                        if annotation[0].cls:
                            self.annotation_to_annotator[f"<{annotation[0].cls}>"] = (module_name, f_name)
                        self.annotation_description[annotation[0].original_name] = annotation[1]
                        if rule_storage.wildcards:
                            self.wildcard_annotations.append(annotation[0].original_name)
                elif rule_storage.importer and rule_made:
                    self.importers[module_name][f_name] = rule_storage

    def q(self, questions: Union[List[dict], dict], clear: bool = False, save_prompt: bool = True):
        """Ask questions and handle interruptions.

        Args:
            questions: Single dictionary or a list with question dictionaries
            clear: Set to True to clear screen before questioning.
            save_prompt: Set to False to disable asking about saving progress if the user interrupts.

        Returns:
            Dictionary with answers
        """
        if clear:
            clear_screen()
        if isinstance(questions, dict):
            questions = [questions]

        # Wrap and indent question
        max_width = min(console.size[0], 80)
        tw1 = textwrap.TextWrapper(width=max_width, break_long_words=False, subsequent_indent="  ")
        tw2 = textwrap.TextWrapper(width=max_width, break_long_words=False, initial_indent="  ", subsequent_indent="  ")
        for q in questions:
            q["message"] = "\n".join(
                tw1.fill(line) if i == 0 else tw2.fill(line) for i, line in enumerate(q["message"].splitlines()))

        answer = prompt(questions, style=style)

        # Handle interruptions
        if not answer:
            if save_prompt:
                if prompt([{
                    "type": "confirm",
                    "name": "answer",
                    "message": "Do you want to save your progress so far to be able to resume the wizard later?"
                }], style=style).get("answer"):
                    self.save_config()
            sys.exit()
        return answer

    @staticmethod
    def set_defaults(questions: Union[List[dict], dict]):
        """Add default values to questions based on existing config."""

        def handle_checkbox_choices(choices, config_value):
            """Mark values as selected based on existing config value."""
            for i, item in enumerate(choices):
                if isinstance(item, dict) and item["value"] in config_value:
                    item["checked"] = True
                elif item in config_value:
                    choices[i] = {"name": item, "value": item, "checked": True}
            return choices

        def checkbox_choices_wrapper(f, config_value):
            """Wrap functions used as choices."""
            def new_f(answers: dict):
                """Call original function and handle any checkboxes."""
                return handle_checkbox_choices(f(answers), config_value)
            return new_f

        if isinstance(questions, dict):
            questions = [questions]
        for question in questions:
            try:
                config_value = config.get(question["name"])
            except TypeError:
                config_value = None
            if config_value is not None:
                question_type = question["type"]
                if question_type in ("text", "password", "input"):
                    question["default"] = config_value
                elif question_type in ("select", "list") and question.get("choices"):
                    default_obj = None
                    for i, item in enumerate(question["choices"]):
                        if (isinstance(item, dict) and item["value"] == config_value) or item == config_value:
                            default_obj = item
                            break
                    if default_obj is not None:
                        question["default"] = default_obj
                elif question_type == "checkbox" and question.get("choices"):
                    if callable(question["choices"]):
                        question["choices"] = checkbox_choices_wrapper(question["choices"], config_value)
                    else:
                        question["choices"] = handle_checkbox_choices(question["choices"], config_value)

        return questions

    def get_module_wizard(self, module_wizard: Tuple[Callable, list, bool],
                          answers: Optional[dict] = None) -> List[dict]:
        """Get wizard from module."""
        args = [answers or {}]
        if module_wizard[2]:
            args.append(self.source_structure)
        questions = module_wizard[0](*args)
        return self.set_defaults(questions)

    def save_config(self):
        """Save config to YAML file."""
        with open("config.yaml", mode="w") as out_file:
            yaml.dump({k: v for k, v in self.corpus_config.items() if not k.startswith("_")}, out_file)
        print("Your corpus configuration has been saved as 'config.yaml'.")

    def load_config(self):
        """Load default config and any existing corpus config."""
        if os.path.isfile(self.config_file):
            use_config_file = self.q({
                "type": "confirm",
                "name": "answer",
                "message": "A corpus configuration file with the name '{}' already exists in the current directory. "
                           "Its contents will be used by the wizard where possible. If you'd rather start with a "
                           "clean slate, abort now and remove or rename the old config file before starting the wizard "
                           "again. Select Y to continue or N to abort.".format(paths.config_file)
            }, clear=True, save_prompt=False)["answer"]
            if use_config_file:
                with open(self.config_file) as f:
                    self.corpus_config = yaml.load(f, Loader=yaml.FullLoader)
                config.load_config(self.config_file)
            else:
                sys.exit()
        else:
            # Load default config
            config.load_config(None)

    def update_config(self, answers: dict):
        """Add answers to corpus_config dict and update full config."""
        for answer in answers:
            config.set_value(answer, answers[answer], config_dict=self.corpus_config)
        config.update_config(self.corpus_config)

    def prerequisites(self):
        """Ask initial question to check prerequisites."""
        ready = self.q({
            "type": "confirm",
            "name": "ready",
            "message": "This wizard will take you through the steps to create a configuration file for your corpus.\n\n"
                       "You may abort the process at any time by pressing Ctrl-C, which will also allow you to save "
                       "most of your progress and continue later.\n\n"
                       "Please note that this wizard is only meant to get you started, and doesn't cover all of "
                       "Sparv's functionality. For more advanced features, refer to the user manual.\n\n"
                       "Before we begin, make sure of the following:\n\n"
                       "* The current location is the directory you want to use for your corpus:\n"
                       f"  {self.here}\n\n"
                       "* The source files (i.e. the input text) are located in a sub-directory to the current "
                       "location.\n\n"
                       "* Your source files are all using the same file format, same file extension and (if "
                       "applicable) the same markup.\n\n"
                       "Is all of the above true?"
        }, clear=True, save_prompt=False)

        if not ready["ready"]:
            sys.exit()

    def run(self):
        """Run the Sparv corpus set-up wizard."""
        # Load default config and any existing corpus config
        self.load_config()

        # Temporarily unset corpus language to allow all modules to be loaded
        language = config.get("metadata.language")
        config.set_value("metadata.language", None)

        # Load all available annotators
        self.update_annotators()

        # Restore language
        config.set_value("metadata.language", language)

        # Build module wizard index
        wizard_from_config = {}
        wizard_from_module = defaultdict(set)
        for w in registry.wizards:
            for config_variable in w[1]:
                wizard_from_config[config_variable] = w
                wizard_from_module[config_variable.split(".")[0]].add(w)

        # Initial question to check prerequisites
        self.prerequisites()

        # Start with metadata questions
        questions = []
        for w in wizard_from_module["metadata"]:
            questions.extend(self.get_module_wizard(w))

        self.update_config(self.q(questions, clear=True))

        # Importer choice
        questions = []
        for w in wizard_from_module["import"]:
            questions.extend(self.get_module_wizard(w))

        self.update_config(self.q(questions))

        # Now that the user has selected a language, update the class dict in registry...
        for cls, targets in registry.all_module_classes[config.get("metadata.language")].items():
            registry.annotation_classes["module_classes"][cls].extend(targets)

        # ...and rebuild annotator list
        self.update_annotators()

        # Ask user if they want to scan source files
        self.scan_source()

        # Choose document annotation
        self.select_document_annotation()

        # Select source annotations to keep
        questions = []
        for w in wizard_from_module["export"]:
            questions.extend(self.get_module_wizard(w))

        self.update_config(self.q(questions))

        # Parse annotations from existing config
        selected_annotations = defaultdict(dict)
        self.parse_config_annotations(selected_annotations)

        # Select annotations
        annotator_max_len = self.select_annotations(selected_annotations)

        # Select classes if needed
        has_class_choices = self.select_classes(selected_annotations)

        # Select wildcards if needed
        has_wildcard_choices = self.select_wildcards(selected_annotations)

        # Add selected annotations to config
        self.update_export_annotations(selected_annotations)

        # Set config variables
        self.edit_config(selected_annotations, annotator_max_len)

        # We're done collecting the required data. Let the user edit further if they want to.
        while True:
            choices = [
                {
                    "name": DONE,
                    "value": "done"
                }
            ]

            if has_class_choices:
                choices.append({
                    "name": "Edit class choices",
                    "value": "class"
                })
            if has_wildcard_choices:
                choices.append({
                    "name": "Edit wildcard references",
                    "value": "wildcard"
                })
            choices.append({
                "name": "Edit annotator configurations",
                "value": "config"
            })

            choice = self.q({
                "name": "choice",
                "type": "select",
                "choices": choices,
                "message": "All the necessary data has been collected, but you may do further customization by "
                           "selecting one of the options below."
            }, clear=True)["choice"]

            if choice == "done":
                break
            elif choice == "class":
                has_class_choices = self.select_classes(selected_annotations, always_ask=True)
            elif choice == "wildcard":
                has_wildcard_choices = self.select_wildcards(selected_annotations, always_ask=True)
                self.update_export_annotations(selected_annotations)
            elif choice == "config":
                self.edit_config(selected_annotations, annotator_max_len, show_optional=True)

        self.save_config()

    def select_document_annotation(self):
        """Ask user for document annotation."""
        doc_annotation = self.q(self.set_defaults({
            "type": "select",
            "name": "import.document_annotation",
            "message": "What is the name of the existing annotation in your source files that encapsulates a "
                       "'document'? This is the text unit for which all document level annotations will apply. "
                       "Usually, no text should exist outside of this annotation.",
            "choices": self.source_structure.get_plain_annotations(self.corpus_config) + [{
                "name": "Enter manually",
                "value": "__sparv_manual_entry"
            }]
        }))
        if doc_annotation["import.document_annotation"] == "__sparv_manual_entry":
            doc_annotation = self.q({
                "type": "text",
                "name": "import.document_annotation",
                "message": "Annotation name, e.g. 'text' or  ̈́document':",
                "validate": lambda x: bool(re.match(r"^\S+$", x))
            })
        self.update_config(doc_annotation)

    def scan_source(self):
        """Create a SourceStructureParser instance and offer to scan source files if possible."""
        # Create instance of SourceStructureParser class (if available)
        importer_module, _, importer_function = config.get("import.importer").partition(":")
        source_structure_class = registry.modules[importer_module].functions[importer_function]["structure"]
        do_scan = False
        if source_structure_class:
            self.source_structure = source_structure_class(Path(config.get("import.source_dir")))
            do_scan = self.q([{
                "type": "confirm",
                "name": "answer",
                "message": "The selected importer may scan your source files to determine their structure. This may be "
                           "convenient if there is a lot of existing markup that you want to refer to later in the "
                           "wizard. If you skip this step, you will have to type them in by hand instead. "
                           "Do you want to go ahead with a scan?"
            }])["answer"]
            if do_scan:
                # Run the structure setup wizard
                setup_wizard = self.source_structure.setup()
                if setup_wizard:
                    answers = self.q(setup_wizard)
                    self.source_structure.answers = answers

                # Perform the scan
                self.source_structure.get_annotations(self.corpus_config)
        if not do_scan:
            self.source_structure = BasicSourceStructure(Path(config.get("import.source_dir")))
            self.source_structure.annotations = self.importers[importer_module][importer_function].import_outputs or []

    def update_export_annotations(self, selected_annotations):
        """Add selected annotations to corpus config."""
        annotations = []
        for module in selected_annotations:
            for f_name in selected_annotations[module]:
                for ann in selected_annotations[module][f_name]:
                    value = ann["annotation"]
                    if "wildcards" in ann:
                        # Replace wildcards with values
                        for wc, wcval in ann["wildcards"].items():
                            value = re.sub(f"{{{wc}}}", wcval, value)
                    annotations.append(value)
        config.set_value("export.annotations", annotations, config_dict=self.corpus_config)

    def edit_config(self, selected_annotations, annotator_max_len, show_optional: bool = False):
        """Ask the user for required config variables."""

        def get_dependencies(module, f):
            """Recursively get all annotators needed by an annotator."""
            if used_annotators[module].get(f) is not None:
                return
            used_annotators[module].setdefault(f, {})
            for input_file in self.snake_storage.all_annotators[module][f]["rule"].inputs:
                if input_file in self.output_to_annotators:
                    for annotator in self.output_to_annotators[input_file]:
                        get_dependencies(*annotator)

        config_annotator = None

        while True:
            # We need to reload annotators in case any configuration has changed
            config.update_config(self.corpus_config)
            self.update_annotators()

            # Find all dependencies for the selected annotations
            used_annotators = defaultdict(dict)
            for module in selected_annotations:
                for f_name in selected_annotations[module]:
                    if selected_annotations[module][f_name]:
                        get_dependencies(module, f_name)

            missing_configs = False

            # Check for any config variables that MUST be set (i.e. they have no default values we can use)
            for module in used_annotators:
                for f_name in used_annotators[module]:
                    missing_config = self.snake_storage.all_annotators[module][f_name]["rule"].missing_config
                    if any(cfg for cfg in missing_config if not cfg.startswith("<")):
                        missing_configs = True
                        config_values = self.q([
                            {
                                "type": "text",
                                "name": config_key,
                                "message": "The following config variable needs to be set.\n"
                                           "Description: {}\n{}:".format(config.get_config_description(config_key),
                                                                         config_key)
                            } for config_key in missing_config if not config_key.startswith("<")
                        ], clear=True)

                        for key, value in config_values.items():
                            config.set_value(key, value)
                            config.set_value(key, value, config_dict=self.corpus_config)
            if missing_configs:
                continue

            if not show_optional:
                return

            config_annotators = []
            preselected = None
            for module in sorted(used_annotators):
                for a in sorted(used_annotators[module]):
                    config_annotators.append({
                        "name": "{:{width}} {}  {}".format(
                            "{}:{}".format(module, a),
                            "({})".format(len(selected_annotations[module].get(a, []))) if
                            selected_annotations[
                                module].get(a) else "   ",
                            self.snake_storage.all_annotators[module][a]["rule"].description,
                            width=annotator_max_len + (
                                0 if not self.snake_storage.all_annotators[module][a][
                                    "rule"].configs else 2)),
                        "value": (module, a),
                        "short": "{}:{}".format(module, a),
                        "disabled": not self.snake_storage.all_annotators[module][a]["rule"].configs
                    })
                    if config_annotator == (module, a):
                        preselected = config_annotators[-1]

            config_annotator = self.q(dict({
                "type": "select",
                "name": "annotator",
                "message": "The following annotators will be used for your corpus, either directly or indirectly by the"
                           " annotators you selected. You may edit their config variables if you wish.",
                "choices": [{
                    "name": DONE,
                    "value": "_done"
                }] + config_annotators
            }, **{"default": preselected} if preselected else {}), clear=True)["annotator"]

            if config_annotator == "_done":
                break
            else:
                module_name, f_name = config_annotator
                max_cfg_len = max(len(cfg) for cfg in
                                  self.snake_storage.all_annotators[module_name][f_name]["rule"].configs)
                config_choice = None
                preselected_key = None
                while True:
                    config_choices = []
                    for cfg in self.snake_storage.all_annotators[module_name][f_name]["rule"].configs:
                        config_choices.append({
                            "name": "{:{width}}  {}".format(cfg, config.get_config_description(cfg),
                                                            width=max_cfg_len),
                            "value": cfg
                        })
                        if config_choice == cfg:
                            preselected_key = config_choices[-1]

                    config_choice = self.q(dict({
                        "type": "select",
                        "name": "config",
                        "message": "What configuration variable do you want to edit?",
                        "choices": [
                           {
                               "name": DONE,
                               "value": "_done"
                           }
                        ] + config_choices
                    }, **{"default": preselected_key} if preselected_key else {}), clear=True)["config"]

                    if config_choice == "_done":
                        break
                    else:
                        config_value = self.q([{
                            "type": "text",
                            "name": "value",
                            "default": config.get(config_choice) or "",
                            "message": "Set value of config variable '{}':".format(config_choice)
                        }])["value"]

                        # Only save value if changed
                        if config_value != (config.get(config_choice) or ""):
                            config.set_value(config_choice, config_value)
                            config.set_value(config_choice, config_value, config_dict=self.corpus_config)

    def select_wildcards(self, selected_annotations, always_ask: bool = False) -> bool:
        """Find any annotations with wildcards and prompt the user to define values for these.

        Returns True if there are wildcards, otherwise False.
        """
        has_wildcards = False
        full_annotations = set()
        plain_annotations = set()
        attributes = set()
        for annotation in self.annotation_to_annotator:
            # Skip classes
            if re.match(r"<[^<>]+>$", annotation):
                continue
            plain_annotation, _, attribute = annotation.partition(":")
            if "{" not in annotation:
                full_annotations.add(annotation)
            if "{" not in plain_annotation:
                plain_annotations.add(plain_annotation)
            if "{" not in attribute:
                attributes.add(attribute)
        for cls in registry.annotation_classes["module_classes"]:
            if ":" not in cls:
                plain_annotations.add(f"<{cls}>")
            else:
                full_annotations.add(f"<{cls}>")
        for module in selected_annotations:
            for f_name in selected_annotations[module]:
                if selected_annotations[module][f_name]:
                    wildcards = self.snake_storage.all_annotators[module][f_name]["rule"].wildcards
                    if wildcards:
                        has_wildcards = True
                        wc_dict = {wc.name: wc for wc in wildcards}
                        wildcard_max_len = max([len(wc.name) for wc in wildcards])
                        selected_wildcards = {}
                        for a in selected_annotations[module][f_name]:
                            if "wildcards" in a:
                                selected_wildcards.update(a["wildcards"])
                        if all(selected_wildcards.get(wc) for wc in wildcards) and not always_ask:
                            continue
                        while True:
                            output_list = "\n".join(f"  {a[0].original_name}" for a in
                                                    self.snake_storage.all_annotators[module][f_name]["annotations"])
                            wc_choice = self.q({
                                "type": "select",
                                "name": "wc",
                                "choices": [{
                                    "value": wc.name,
                                    "name": "{:{width}}  {}".format(
                                        wc.name,
                                        selected_wildcards.get(wc.name, ""),
                                        width=wildcard_max_len)
                                } for wc in wildcards] + [
                                    {
                                        "value": "_done",
                                        "name": DONE,
                                        "disabled": not all(selected_wildcards.get(wc) for wc in wildcards)
                                    }
                                ],
                                "message": "You have selected to use the following annotator:\n\n"
                                           f"  {module}:{f_name}   "
                                           f"{self.snake_storage.all_annotators[module][f_name]['description']}\n\n"
                                           f"It produces the following annotations:\n\n{output_list}\n\n"
                                           "The annotations refer to other annotations by using curly braces. "
                                           "To continue you need to select values for these references."
                            }, clear=True)["wc"]

                            if wc_choice == "_done":
                                break

                            if wc_dict[wc_choice].type == Wildcard.ANNOTATION:
                                choices = plain_annotations
                            elif wc_dict[wc_choice].type == Wildcard.ATTRIBUTE:
                                choices = attributes
                            elif wc_dict[wc_choice].type == Wildcard.ANNOTATION_ATTRIBUTE:
                                choices = full_annotations
                            else:
                                choices = []

                            wc_val_max = max(map(len, choices))

                            def get_description(ann: str):
                                """Get description of annotation."""
                                desc = None
                                if ann.startswith("<") and ann.endswith(">"):
                                    desc = registry._expand_class(ann[1:-1])
                                    if desc:
                                        desc = "Class referring to " + desc
                                if not desc:
                                    desc = self.annotation_description.get(ann)
                                return desc or "No description available"

                            wcv_choices = []
                            preselected = None
                            for annotation in sorted(choices):
                                item = {
                                    "name": "{:{width}}  {}".format(
                                        annotation,
                                        get_description(annotation),
                                        width=wc_val_max),
                                    "value": annotation
                                }
                                if selected_wildcards.get(wc_choice) == annotation:
                                    preselected = item
                                wcv_choices.append(item)

                            wcv_choice = self.q({
                                "type": "select",
                                "name": "value",
                                "message": f"Select the value you want to use for the '{wc_choice}' reference:",
                                "choices": wcv_choices,
                                "default": preselected
                            }, clear=True)["value"]
                            selected_wildcards[wc_choice] = wcv_choice
                        for annotation in selected_annotations[module][f_name]:
                            if "{" in annotation["annotation"]:
                                annotation["wildcards"] = selected_wildcards
        return has_wildcards

    def select_classes(self, selected_annotations, always_ask: bool = False) -> bool:
        """Find if any dependencies are using classes with multiple options. If so, ask the user which to use.

        Returns True if there are multiple options, otherwise False.
        """
        has_choices = False
        available_classes = registry.annotation_classes["module_classes"]
        for module in selected_annotations:
            for f_name in selected_annotations[module]:
                if selected_annotations[module][f_name]:
                    for cls in self.snake_storage.all_annotators[module][f_name]["rule"].classes:
                        if len(available_classes.get(cls, [])) > 1:
                            has_choices = True
                            if not always_ask and config.get(f"classes.{cls}"):
                                continue
                            max_cls_len = max(map(len, available_classes[cls]))
                            selected_class = self.q(self.set_defaults([
                                {
                                    "type": "select",
                                    "name": f"classes.{cls}",
                                    "choices": [{
                                        "name": "{:{width}}  Provided by {}".format(
                                            c,
                                            ":".join(self.annotation_to_annotator.get(c, ())),
                                            width=max_cls_len),
                                        "value": c
                                    } for c in available_classes[cls]],
                                    "message": "One of the annotations used by your corpus is referring to another "
                                               f"annotation using the class <{cls}>. This annotation can be "
                                               "provided by more than one annotator. Please select which one you want "
                                               "to use:"
                                }
                            ]), clear=True)

                            self.update_config(selected_class)
                            self.update_annotators()
        return has_choices

    def select_annotations(self, selected_annotations) -> int:
        """Let the user select annotators and annotations to use."""
        max_len = max(
            len(module + f_name) + 1 for module in self.snake_storage.all_annotators for f_name in
            self.snake_storage.all_annotators[module])
        annotator_choice = None
        while True:
            annotators = []
            preselected = None
            for module in self.snake_storage.all_annotators:
                for a in self.snake_storage.all_annotators[module]:
                    annotators.append({
                        "name": "{:{width}} {}  {}".format(
                            "{}:{}".format(module, a),
                            "({})".format(len(selected_annotations[module].get(a, []))) if
                            selected_annotations[
                                module].get(a) else "   ",
                            self.snake_storage.all_annotators[module][a]["rule"].description,
                            width=max_len),
                        "value": (module, a),
                        "short": "{}:{}".format(module, a)
                    })
                    if annotator_choice == (module, a):
                        preselected = annotators[-1]

            annotator_choice = self.q(dict({
                "type": "select",
                "name": "annotator",
                "message": "The following is a list of annotators available for the language you've chosen. "
                           "Select an annotator below to display its available annotations. "
                           "Select DONE when you're done.",
                "choices": [
                               {
                                   "name": DONE,
                                   "value": "_done"
                               },
                           ] + annotators
                }, **{"default": preselected} if preselected else {}), clear=True)["annotator"]
            if not annotator_choice == "_done":
                module, annotator = annotator_choice
                max_len2 = max(len(a[0].original_name) for a in
                               self.snake_storage.all_annotators[module][annotator]["annotations"])
                annotations_choice = self.q([
                    {
                        "name": "annotations",
                        "type": "checkbox",
                        "message": "Use space to select the annotations you want below, and press enter to return:",
                        "choices": [
                            {
                                "name": "{:{width}}    {}".format(annotation[0].original_name,
                                                                  annotation[1] or "No description available",
                                                                  width=max_len2),
                                "value": annotation[0].original_name,
                                "checked": annotation[0].original_name in [a["annotation"] for a in
                                                                           selected_annotations[module].get(annotator,
                                                                                                            [])]
                            } for annotation in
                            self.snake_storage.all_annotators[module][annotator]["annotations"]
                        ]
                    }
                ], clear=True)["annotations"]
                selected_annotations[module][annotator] = []
                for annotation in annotations_choice:
                    selected_annotations[module][annotator].append({"annotation": annotation})
            else:
                break
        return max_len

    def parse_config_annotations(self, selected_annotations) -> None:
        """Parse selected annotations from existing config."""
        for annotation in self.corpus_config.get("export", {}).get("annotations", []):
            module_name = None
            f_name = None
            wildcards = None
            try:
                module_name, f_name = self.annotation_to_annotator[annotation]
            except KeyError:
                # Possibly a wildcard annotation
                for wc_ann in self.wildcard_annotations:
                    wcs = re.findall(r"{([^}]+)}", wc_ann)
                    ann_re = re.sub(r"{[^}]+}", "(.+?)", wc_ann)
                    wc_vals = re.match(ann_re + "$", annotation)
                    if wc_vals:
                        wildcards = dict(zip(wcs, wc_vals.groups()))
                        module_name, f_name = self.annotation_to_annotator[wc_ann]
                        annotation = wc_ann
                        break

            if f_name:
                selected_annotations[module_name].setdefault(f_name, [])
                val = {"annotation": annotation}
                if wildcards:
                    val["wildcards"] = wildcards
                selected_annotations[module_name][f_name].append(val)
            else:
                print(f"Could not parse the annotation '{annotation}'.")
                sys.exit(1)


if __name__ == "__main__":
    wizard = Wizard()
    wizard.run()
